# PyTorch function regression

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader, random_split
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import clear_output

# -----------------------------
# 1) Generate data
# -----------------------------
np.random.seed(42)
x = np.linspace(-5, 5, 200).reshape(-1,1)
y = np.sin(x) + 0.3*x + 0.1*np.random.randn(*x.shape)

# -----------------------------
# 2) Normalize data
# -----------------------------
x_mean, x_std = x.mean(), x.std()
y_mean, y_std = y.mean(), y.std()

x_norm = (x - x_mean)/x_std
y_norm = (y - y_mean)/y_std

# -----------------------------
# 3) Convert to tensors
# -----------------------------
X = torch.tensor(x_norm, dtype=torch.float32)
Y = torch.tensor(y_norm, dtype=torch.float32)

# -----------------------------
# 4) Dataset and DataLoader
# -----------------------------
dataset = TensorDataset(X, Y)
train_size = int(0.8 * len(dataset))
val_size = len(dataset) - train_size
train_dataset, val_dataset = random_split(dataset, [train_size, val_size])

batch_size = 32
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=batch_size)

# -----------------------------
# 5) Define neural network
# -----------------------------
class SimpleRegressor(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(1, 16),
            nn.ReLU(),
            nn.Linear(16, 16),
            nn.ReLU(),
            nn.Linear(16, 1)
        )
    def forward(self, x):
        return self.net(x)

# -----------------------------
# 6) Instantiate model, loss, optimizer, scheduler
# -----------------------------
device = "cuda" if torch.cuda.is_available() else "cpu"
model = SimpleRegressor().to(device)
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)
scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=10, verbose=True)

# -----------------------------
# 7) Training loop with early stopping and live plotting
# -----------------------------
epochs = 500
patience = 20
best_val_loss = np.inf
trigger_times = 0

train_losses = []
val_losses = []

plt.ion()  # interactive plotting
fig, ax = plt.subplots(figsize=(10,5))

for epoch in range(epochs):
    # ----- Training -----
    model.train()
    running_loss = 0.0
    for xb, yb in train_loader:
        xb, yb = xb.to(device), yb.to(device)
        optimizer.zero_grad()
        y_pred = model(xb)
        loss = criterion(y_pred, yb)
        loss.backward()
        optimizer.step()
        running_loss += loss.item() * xb.size(0)
    train_loss = running_loss / train_size
    train_losses.append(train_loss)
    
    # ----- Validation -----
    model.eval()
    val_running_loss = 0.0
    with torch.no_grad():
        for xb, yb in val_loader:
            xb, yb = xb.to(device), yb.to(device)
            y_pred = model(xb)
            loss = criterion(y_pred, yb)
            val_running_loss += loss.item() * xb.size(0)
    val_loss = val_running_loss / val_size
    val_losses.append(val_loss)
    
    # Scheduler step
    scheduler.step(val_loss)
    
    # Print every 50 epochs
    if (epoch+1) % 50 == 0:
        print(f"Epoch {epoch+1}/{epochs} - Train Loss: {train_loss:.6f} - Val Loss: {val_loss:.6f}")
    
    # Early stopping
    if val_loss < best_val_loss:
        best_val_loss = val_loss
        trigger_times = 0
        torch.save(model.state_dict(), "best_model.pth")
    else:
        trigger_times += 1
        if trigger_times >= patience:
            print(f"Early stopping at epoch {epoch+1}")
            break

    # ----- Live plotting -----
    if (epoch+1) % 10 == 0:
        model.eval()
        with torch.no_grad():
            X_tensor = torch.tensor(x_norm, dtype=torch.float32).to(device)
            y_hat_norm = model(X_tensor).cpu().numpy()
            y_hat = y_hat_norm * y_std + y_mean
        clear_output(wait=True)
        ax.clear()
        ax.scatter(x, y, label="Original data")
        ax.plot(x, y_hat, color='red', label="NN prediction")
        ax.set_title(f"Epoch {epoch+1}")
        ax.legend()
        plt.pause(0.1)

plt.ioff()

# -----------------------------
# 8) Load best model
# -----------------------------
model.load_state_dict(torch.load("best_model.pth"))
model.eval()

# -----------------------------
# 9) Final predictions
# -----------------------------
with torch.no_grad():
    X_tensor = torch.tensor(x_norm, dtype=torch.float32).to(device)
    y_hat_norm = model(X_tensor).cpu().numpy()
    y_hat = y_hat_norm * y_std + y_mean

# -----------------------------
# 10) Visualization final
# -----------------------------
plt.figure(figsize=(12,5))

plt.subplot(1,2,1)
plt.scatter(x, y, label="Original data")
plt.plot(x, y_hat, color='red', label="NN prediction")
plt.legend()
plt.title("Function regression - final prediction")

plt.subplot(1,2,2)
plt.plot(train_losses, label="Train Loss")
plt.plot(val_losses, label="Validation Loss")
plt.xlabel("Epoch")
plt.ylabel("MSE Loss")
plt.legend()
plt.title("Training and Validation Loss")
plt.show()
