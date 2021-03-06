import sys, re, os, shutil
from tkinter import*
import tkinter.filedialog
import tkinter.messagebox
import win32com.client


temp_file = ''
path = ''
select_folder = 'Select folder ===>'
all_dictionarys = {
  '0': ['байт', 'byte', 'Byte', 'Байт'],
  '1': ['КБ', 'kB', 'KB', 'kb'],
  '2': ['МБ', 'mB', 'MB', 'mb'],
  '3': ['ГБ', 'gB', 'GB', 'gb'],
  '4': ['ТБ', 'tB', 'TB', 'tb']
}


def tf():
    global temp_file
    temp_file = tkinter.filedialog.askdirectory(parent = root, initialdir = os.getcwd(), title = "Select a folder")
    vevod_direct = ''
    kl = 0
    if len(temp_file) <= 55 :
        vevod_direct = temp_file
        lbl.configure(text = vevod_direct + '/') # 55 символов
    else:
        kl = 55 - len(temp_file) 
        vevod_direct = temp_file [0:kl] + '...'
        lbl.configure(text = vevod_direct)
    sort_file.configure(state = NORMAL)


def get_file_metadata(path, filename, metadata): 
    sh = win32com.client.gencache.EnsureDispatch('Shell.Application', 0)
    ns = sh.NameSpace(path.replace('/', '\\'))

    file_metadata = dict()
    item = ns.ParseName(str(filename))
    
    for ind, attribute in enumerate(metadata):
        attr_value = ns.GetDetailsOf(item, ind)
        
        if attr_value:
            file_metadata[attribute] = attr_value

    return file_metadata
    # print(get_file_metadata(folder, filename, metadata))
    # metadata ['Name', 'Size', 'Item type', 'Date modified', 'Date created']


def convert_size_to_str(p):
    for size in all_dictionarys:
        if p[1] in all_dictionarys[size]:
            return float(p[0].replace(',', '.'))* 1024**int(size)


def name_of_folder_of_size(in_path, in_size):
    if in_size <= 10485760:
        return in_path + "/less than 10 MB"
    elif 10485760 < in_size <= 31457280:
        return in_path + "/10 MB to 30 MB"
    elif 31457280 < in_size <= 104857600:
        return in_path + "/30 MB to 100 MB"
    elif 104857600 < in_size <= 524288000:
        return in_path + "/100 MB to 500 MB"
    elif 524288000 < in_size <= 1073741824:
        return in_path + "/500 MB to 1 GB"
    elif 1073741824 < in_size:
        return in_path + "/more than 1 GB"


def meta_sorting_core(sorting_func):
    count_file = 0

    path = temp_file  
    files = os.listdir(path) 
    for file_name in files:
        if os.path.splitext(file_name)[1][1:] == "": 
            continue
        
        file_data = get_file_metadata(path, file_name, ['Name', 'Size', 'Item type', 'Date modified', 'Date created']) 

        path1 = sorting_func(path, file_data)

        if lang.get() == 1:                         
            if os.path.splitext(file_data['Name'])[0] == None:
                continue

        if lang.get() == 2:                         
            if not size_name[0][0].isdigit:
                continue

        if lang.get() == 3:                         
            if file_data['Date modified'] == None:
                continue
        
        if lang.get() == 4:                         
            if file_data['Date created'] == None:
                continue
        

        if not os.path.exists(path1): 
            os.mkdir(path1) 
        
        os.chdir(path) 
        shutil.move(path + '/' + file_name, path1) 
        
        count_file += 1 
    if count_file == 0:
        tkinter.messagebox.showinfo(title="Attention", message="There is nothing to sort in the folder")
    if len(temp_file) > 0 and count_file != 0:
        tkinter.messagebox.showinfo(title="Successfully", message="Files sorted")

def sort_by_size():
    meta_sorting_core(size_sorting_func)


def sort_by_date_modified():
    meta_sorting_core(date_modified_sorting_func)


def sort_by_date_created():
    meta_sorting_core(date_created_sorting_func)


def sort_by_ext():
    meta_sorting_core(ext_sorting_func)


def sort_by_first_letter():
    meta_sorting_core(first_letter_sorting_func)


def size_sorting_func(ppath, file_data):
    global size_name             
    size_name = file_data['Size'].split(' ')  
    print(os.path.splitext(file_data['Name'])[1][1:])
    
    return name_of_folder_of_size(ppath, convert_size_to_str(size_name))


def date_modified_sorting_func(ppath, file_data):
    global data_modified            
    data_modified = file_data['Date modified'][0:10]
    
    return ppath + '/' + data_modified


def date_created_sorting_func(ppath, file_data):
    global data_created            
    data_created = file_data['Date created'][0:10]
    
    return ppath + '/' + data_created


def ext_sorting_func(ppath, file_data):            
    ext_name = os.path.splitext(file_data['Name'])[1][1:].upper()
    
    return ppath + '/' + ext_name


def first_letter_sorting_func(ppath, file_data):
    first_letter_name = os.path.splitext(file_data['Name'])[0][0].upper()
    
    return ppath + '/' + first_letter_name


def sort_final():
    if lang.get() == 0:
        sort_by_ext()
    elif lang.get() == 1:
        sort_by_first_letter()
    elif lang.get() == 2:
        sort_by_size()
    elif lang.get() == 3:
        sort_by_date_modified()
    elif lang.get() == 4:
        sort_by_date_created()
 
    
root = Tk()

root.title('Parallax')
root.geometry('400x120')

direct = Entry(root,width=45, state='disabled', text = 'Specify the path', bd = 5, relief = GROOVE)
direct.place(x = 10, y = 20) 

lbl = Label(root, text=select_folder, font=("Arial Bold", 7), bg='white')  
lbl.place(x = 15, y = 23)

btn = Button(root, text="Specify the path", bd = 2, relief = GROOVE, command = tf)
btn.place(x = 300, y = 20)

lang = IntVar()

ext_checkbutton = Radiobutton(text="Extension", value=0, variable=lang, padx=15, pady=10)
ext_checkbutton.place(x = 140, y = 50)

first_letter_checkbutton = Radiobutton(text="1st letter", value=1, variable=lang, padx=15, pady=10)
first_letter_checkbutton.place(x = 0, y = 80)

size_checkbutton = Radiobutton(text="Size", value=2, variable=lang, padx=15, pady=10)
size_checkbutton.place(x = 260, y = 80)

date_modified_checkbutton = Radiobutton(text="Date modified", value=3, variable=lang, padx=15, pady=10)
date_modified_checkbutton.place(x = 0, y = 50)

date_created_checkbutton = Radiobutton(text="Date created", value=4, variable=lang, padx=15, pady=10)
date_created_checkbutton.place(x = 260, y = 50)

sort_file = Button(root, text="Sort", bd = 2, relief = GROOVE, state=DISABLED, command = sort_final)
sort_file.place(x = 180, y = 90)

root.resizable(width=False, height=False)

root.mainloop()