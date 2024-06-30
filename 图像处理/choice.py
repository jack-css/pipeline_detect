import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.withdraw()  # 隐藏主窗口

messagebox.showinfo("信息", "这是一个信息提示框")
result = messagebox.askyesno("确认", "是否继续？")
if result:
    print("用户选择继续操作")
else:
    print("用户取消操作")
