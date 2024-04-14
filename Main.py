from tkinter import messagebox
from tkinter import *
from tkinter import simpledialog
import tkinter
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from Block import *
from Blockchain import *
from hashlib import sha256
import os
import datetime
import webbrowser

main = Tk()
main.title('Blockchain Based Product Authentication And Counterfeit Elimination')
main.geometry("1300x1200")

global filename

blockchain = Blockchain()
if os.path.exists('blockchain_contract.txt'):
    with open('blockchain_contract.txt', 'rb') as fileinput:
        blockchain = pickle.load(fileinput)
    fileinput.close()

def addProduct():
    global filename
    text.delete('1.0', END)
    filename = askopenfilename(initialdir = "original_barcodes")
    with open(filename,"rb") as f:
        bytes = f.read()
    f.close()
    pid = tf1.get()
    name = tf2.get()
    user = tf3.get()
    address = tf4.get()
    if len(pid) > 0 and len(name) > 0 and len(user) > 0 and len(address) > 0:
        current_time = datetime.datetime.now() 
        digital_signature = sha256(bytes).hexdigest();
        data = pid+"#"+name+"#"+user+"#"+address+"#"+str(current_time)+"#"+digital_signature
        blockchain.add_new_transaction(data)
        hash = blockchain.mine()
        b = blockchain.chain[len(blockchain.chain)-1]
        text.insert(END,"Blockchain Previous Hash : "+str(b.previous_hash)+"\nBlock No : "+str(b.index)+"\nCurrent Hash : "+str(b.hash)+"\n")
        text.insert(END,"Barcode Blockchain Digital Signature : "+str(digital_signature)+"\n\n")
        blockchain.save_object(blockchain,'blockchain_contract.txt')
        tf1.delete(0, 'end')
        tf2.delete(0, 'end')
        tf3.delete(0, 'end')
        tf4.delete(0, 'end')
    else:
        text.insert(END,"Please enter all details")

def authenticateProduct():
    text.delete('1.0', END)
    filename = askopenfilename(initialdir = "original_barcodes")
    with open(filename,"rb") as f:
        bytes = f.read()
    f.close()
    digital_signature = sha256(bytes).hexdigest();
    flag = True
    for i in range(len(blockchain.chain)):
        if i > 0:
            b = blockchain.chain[i]
            data = b.transactions[0]
            arr = data.split("#")
            if arr[5] == digital_signature:
                output = ''
                text.insert(END,"Uploaded Product Barcode Authentication Successfull\n")
                text.insert(END,"Details extracted from Blockchain after Validation\n\n")
                text.insert(END,"Product ID                   : "+arr[0]+"\n")
                text.insert(END,"Product Name                 : "+arr[1]+"\n")
                text.insert(END,"Company/User Details         : "+arr[2]+"\n")
                text.insert(END,"Address Details              : "+arr[3]+"\n")
                text.insert(END,"Scan Date & Time             : "+arr[4]+"\n")
                text.insert(END,"Product Barcode Digital Sign : "+arr[5]+"\n")
                output='<html><body><table border=1>'
                output+='<tr><th>Block No</th><th>Product ID</th><th>Product Name</th><th>Company/User Details</th><th>Address Details</th><th>Scan Date & Time</th>'
                output+='<th>Product Barcode Digital Signature</th></tr>'
                output+='<tr><td>'+str(i)+'</td><td>'+arr[0]+'</td><td>'+arr[1]+'</td><td>'+arr[2]+'</td><td>'+arr[3]+'</td><td>'+arr[4]+'</td><td>'+arr[5]+'</td></tr>'
                f = open("output.html", "w")
                f.write(output)
                f.close()
                webbrowser.open("output.html",new=1)
                flag = False
                break
    if flag:
        text.insert(END,"Uploaded Product Barcode Authentication Failed")

def searchProduct():
    text.delete('1.0', END)
    pid = tf1.get()
    flag = True
    if len(pid) > 0:
        for i in range(len(blockchain.chain)):
            if i > 0:
                b = blockchain.chain[i]
                data = b.transactions[0]
                arr = data.split("#")
                if arr[0] == pid:
                    output = ''
                    text.insert(END,"Product Details extracted from Blockchain using Product ID : "+pid+"\n\n")
                    text.insert(END,"Product ID                   : "+arr[0]+"\n")
                    text.insert(END,"Product Name                 : "+arr[1]+"\n")
                    text.insert(END,"Company/User Details         : "+arr[2]+"\n")
                    text.insert(END,"Address Details              : "+arr[3]+"\n")
                    text.insert(END,"Scan Date & Time             : "+arr[4]+"\n")
                    text.insert(END,"Product Barcode Digital Sign : "+arr[5]+"\n")
                    output='<html><body><table border=1>'
                    output+='<tr><th>Block No</th><th>Product ID</th><th>Product Name</th><th>Company/User Details</th><th>Address Details</th><th>Scan Date & Time</th>'
                    output+='<th>Product Barcode Digital Signature</th></tr>'
                    output+='<tr><td>'+str(i)+'</td><td>'+arr[0]+'</td><td>'+arr[1]+'</td><td>'+arr[2]+'</td><td>'+arr[3]+'</td><td>'+arr[4]+'</td><td>'+arr[5]+'</td></tr>'
                    f = open("output.html", "w")
                    f.write(output)
                    f.close()
                    webbrowser.open("output.html",new=1)
                    flag = False
                    break
    if flag:
        text.insert(END,"Given product id does not exists")
        
    
    

font = ('times', 15, 'bold')
title = Label(main, text='Blockchain Based Product Authentication And Counterfeit Elimination')
title.config(bg='bisque', fg='purple1')  
title.config(font=font)           
title.config(height=3, width=120)       
title.place(x=0,y=5)

font1 = ('times', 13, 'bold')

l1 = Label(main, text='Product ID :')
l1.config(font=font1)
l1.place(x=50,y=100)

tf1 = Entry(main,width=20)
tf1.config(font=font1)
tf1.place(x=240,y=100)

l2 = Label(main, text='Product Name :')
l2.config(font=font1)
l2.place(x=50,y=150)

tf2 = Entry(main,width=20)
tf2.config(font=font1)
tf2.place(x=240,y=150)

l3 = Label(main, text='Company/User Details :')
l3.config(font=font1)
l3.place(x=50,y=200)

tf3 = Entry(main,width=60)
tf3.config(font=font1)
tf3.place(x=240,y=200)

l4 = Label(main, text='Address Details :')
l4.config(font=font1)
l4.place(x=50,y=250)

tf4 = Entry(main,width=80)
tf4.config(font=font1)
tf4.place(x=240,y=250)

saveButton = Button(main, text="Save Product with Blockchain Entry", command=addProduct)
saveButton.place(x=50,y=300)
saveButton.config(font=font1)

searchButton = Button(main, text="Retrieve Product Data", command=searchProduct)
searchButton.place(x=370,y=300)
searchButton.config(font=font1)

scanButton = Button(main, text="Authenticate Scan", command=authenticateProduct)
scanButton.place(x=590,y=300)
scanButton.config(font=font1)

font1 = ('times', 13, 'bold')
text=Text(main,height=15,width=120)
scroll=Scrollbar(text)
text.configure(yscrollcommand=scroll.set)
text.place(x=10,y=350)
text.config(font=font1)

main.config(bg='pink')
main.mainloop()
