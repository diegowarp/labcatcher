# LABCatcher

LABCatcher is a tool for extracting LAB color values from images without a physical colorimeter. With an intuitive GUI built using Tkinter and OpenCV, users can load images in various formats, select regions of interest, and calculate average LAB colors.

# Features

 - Supports multiple image formats, including RAW (.NEF);
 - Interactive ROI selection for precise color extraction;
 - Converts RGB to LAB using colorspacious;
 - Copy results to clipboard for easy documentation;

# Screenshots

![image](https://github.com/user-attachments/assets/22f85c01-a04d-41bf-82a7-fb14d1a59c9f)


![image](https://github.com/user-attachments/assets/3eeb9629-7738-4bbc-8314-dd6154192daa)


![image](https://github.com/user-attachments/assets/df384feb-8d69-4ded-8987-3ae2866aed25)


![image](https://github.com/user-attachments/assets/5d938e5e-d2ad-4fbe-91d7-ecc11dc7aeef)


## Installation

Install dependencies:

```bash
pip install opencv-python rawpy numpy pyperclip colorspacious

```

Run the application:

```bash
python main.py
```

# License

This project is licensed under the MIT License.

