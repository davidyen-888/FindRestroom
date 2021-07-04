import matplotlib.pyplot as plt  # 顯示圖片
import matplotlib.image as mpimg  # 讀取圖片
import random
import os
import tkinter as tk
from tkinter import filedialog
import shutil
import glob


pathdir = os.path.abspath('.')  # get絕對路徑
path_p = 'pictrue'
path_d = 'data'

# create window

window = tk.Tk()
window.title('成大如廁指南')

# Label

tk.Label(window, text='我是成大如廁指南', font=("Courier New", 24)).grid(row=0, columnspan=3)
tk.Label(window, text='隨機探索', font=("Calibri")).grid(row=1, column=0)  # command = explore
tk.Label(window, text='新增資料', font=("Calibri")).grid(row=2, column=0, rowspan=4)
tk.Label(window, text='請輸入廁所位置: ', font=("Calibri")).grid(row=3, column=1, ipadx=0, ipady=0)
tk.Label(window, text='請輸入星級： ', font=("Calibri")).grid(row=4, column=1)
tk.Label(window, text='請輸入有無衛生紙(有或無)： ', font=("Calibri")).grid(row=5, column=1)
tk.Label(window, text='請輸入廁所簡介： ', font=("Calibri")).grid(row=6, column=1)
tk.Label(window, text='刪除資料', font=("Calibri")).grid(row=7, column=0)
tk.Label(window, text="請輸入要刪除檔案的廁所位置: ", font=("Calibri")).grid(row=7, column=1)
tk.Label(window, text='訊息', font=("Calibri")).grid(row=8, column=0)

# Entry

e1 = tk.Entry(window)
e1.grid(row=3, column=2)
e2 = tk.Entry(window)
e2.grid(row=4, column=2)
e3 = tk.Entry(window)
e3.grid(row=5, column=2)
e4 = tk.Entry(window)
e4.grid(row=6, column=2)
e5 = tk.Entry(window)
e5.grid(row=7, column=2)

# Text
t = tk.Text(window, width=30, font=("Calibri"))
t.grid(row=8, column=1)

# function


def del_text():
    t.delete(1.0, tk.END)
    tk.messagebox.showinfo('訊息', "成功清除訊息欄")


def count_files():
    files_path = os.path.join(pathdir, path_p)
    files_grab = []
    #types = ('*.jpg','*.PNG','*.png','*.GIF')
    for ext in ('*.jpg', '*.PNG', '*.png', '*.GIF'):
        files_grab.extend(glob.glob(os.path.join(files_path, ext)))
    return files_grab


def explore():
    file_list = count_files()
    num = random.randint(1, len(file_list))  # 亂數
    temp = file_list[num - 1]
    name = os.path.basename(temp).split('.')[0]  # 分割字串
    # print("\t探索的目的為 : " + name)
    t.insert(tk.END, '\n探索的目的為:\n\t' + name)

    # 顯示圖片
    pic = mpimg.imread(temp)  # 圖片路徑
    pic.shape
    plt.imshow(pic)
    plt.axis('off')  # 不顯示座標
    plt.ion()
    plt.pause(3)

    # 顯示簡介
    fp = open(os.path.join(pathdir, path_d, name + '.txt'), 'r', encoding='utf8')
    for content in fp:
        if(content == '位置:\n'):
            t.insert(tk.END, '\n位置:')
            content = fp.readline()
            t.insert(tk.END, '\n\t' + content.rstrip())
        elif(content == '星級:\n'):
            t.insert(tk.END, '\n星級:')
            content = fp.readline()
            t.insert(tk.END, '\n\t' + content.rstrip())
        elif(content == '有無衛生紙:\n'):
            t.insert(tk.END, '\n有無衛生紙:')
            content = fp.readline()
            t.insert(tk.END, '\n\t' + content.rstrip())
        elif(content == '廁所簡介:\n'):
            t.insert(tk.END, "\n簡介:")
            content = fp.readline()
            t.insert(tk.END, '\n\t' + content.rstrip() + '\n')
    fp.close()
    # plt.close()


def add():
    if(e1.get() == '' or e2.get() == '' or e3.get() == '' or e4.get() == ''):
        t.insert(tk.END, '\n\t請輸入完整資料\n')
        tk.messagebox.showerror(title='錯誤', message='請輸入完整資料')
        return
    t.insert(tk.END, '\n\t請上傳圖片\n')
    tk.messagebox.showinfo(title='訊息', message='請上傳圖片')
    fpath = filedialog.askopenfilename(defaultextension='.jpg',
                                       filetypes=[('All files', '*.*'), ('PNG pictures', '*.png'), ('JPEG pictures', '*.jpg')])  # 開啟檔案的視窗
    temp1 = fpath
    if(temp1 == ""):  # if沒上傳檔案
        t.insert(tk.END, "\n\t上傳取消\n")
        tk.messagebox.showwarning(title='警告', message='上傳取消')
    else:
        lname = temp1.split('.')[1]  # 副檔名
        fcopy = os.path.join(pathdir, path_p, e1.get() + '.' + lname)
        try:
            shutil.copyfile(fpath, fcopy)
        except BaseException:
            # print("\t無法上傳圖片!")
            t.insert(tk.END, "\t無法上傳圖片!\n")
        # print("\t上傳成功!")
        t.insert(tk.END, "\n\t上傳成功!\n")
        tk.messagebox.showinfo(title='訊息', message='上傳成功!')
        file = open(os.path.join(pathdir, path_d, e1.get() + ".txt"), 'w', encoding='utf8')  # 開一個新的txt

        # 把String寫進檔案
        file.write("位置:\n" + e1.get() + "\n\n")
        file.write("星級:\n" + e2.get() + "\n\n")
        file.write("有無衛生紙:\n" + e3.get() + "\n\n")
        file.write("廁所簡介:\n" + e4.get() + "\n\n")
        file.close()


def delete():
    flag = True
    try:
        os.remove(os.path.join(pathdir, path_d, e5.get() + ".txt"))
    except BaseException:
        t.insert(tk.END, "\n\t無法刪除資料檔案!\n")
        tk.messagebox.showerror(title='錯誤', message='無法刪除資料檔案')
        flag = False

    # 因為不能確定圖片副檔名，所以用glob來找特定名稱的檔案
    dle_pname = os.path.join(pathdir, path_p, e5.get() + '.*')
    str1 = ''.join(glob.glob(dle_pname))  # list轉成string
    try:
        os.remove(str1)
    except BaseException:
        t.insert(tk.END, "\n\t無法刪除圖片檔案!\n")
        tk.messagebox.showerror(title='錯誤', message='無法刪除圖片檔案')
        flag = False
    if flag:
        t.insert(tk.END, "\n\t圖片和資料刪除成功\n")
        tk.messagebox.showinfo(title='訊息', message='成功刪除圖片和資料')

    else:
        t.insert(tk.END, "\n圖片和資料至少有一個沒刪除成功\n")
        tk.messagebox.showwarning(title='警告', message='圖片和資料至少有一個沒刪除成功')


# button

button1 = tk.Button(window, text='探索', command=explore, width=30).grid(row=1, column=1, columnspan=3)
button2 = tk.Button(window, text='新增', command=add, height=8).grid(row=3, column=3, rowspan=4)
button3 = tk.Button(window, text='刪除', command=delete).grid(row=7, column=3)
button4 = tk.Button(window, text='清除訊息', command=del_text, height=10, width=15).grid(row=8, column=2)

window.mainloop()
