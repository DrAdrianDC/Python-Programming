#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 07:48:33 2024

@author: adriandominguezcastro
"""

# QR Code generation using Python

# pip install pyqrcode
# pip install pypng


import pyqrcode
from PIL import Image

# Get the link from the user
link = input("Enter the link to generate QR Code: ")

# Create the QR code
qr_code = pyqrcode.create(link)

# Save the QR code as a PNG file
qr_code.png("QRCode.png", scale=5)  # Save using png() method

# Open and display the saved QR code image
img = Image.open("QRCode.png")
img.show()  # Use show() to display the image


