#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Jpegzilla
# A simple, cross-platform and lightweight graphical user interface for MozJPEG.
# https://github.com/canimar/jpegzilla

import sys, ntpath, os, subprocess, threading, json
import math, platform, shutil, glob, re
import tkinter, tkinter.ttk, tkinter.filedialog

<<<<<<< HEAD
from tkinter import messagebox
from PIL import Image, ImageTk

FNULL = open(os.devnull, 'w')
OS = platform.system()
VER = '0.9'
=======
import webbrowser

from tkinter import messagebox
from PIL import Image, ImageTk
>>>>>>> origin/master

from conf import TEMPDIR, JZ_ICON_TKINTER, VER, OS, DOCS_URL, DEBUG

class jpegzilla:

    def __init__(self):

        # Colors
        self.bg = '#FEFEFE' # Background color
        self.fg = '#000000' # Foreground color
        self.fgdis = '#555555' # Foreground color of disabled element

<<<<<<< HEAD
        self.debug = False
=======
        self.debug = DEBUG
>>>>>>> origin/master

        first_run = False

        # Get current file.
        if (getattr(sys, 'frozen', False)):
            _thisfile = sys.executable
        else:
            _thisfile = __file__

<<<<<<< HEAD
        # Load locale file.
        locale_path = os.path.dirname(os.path.abspath(_thisfile).replace('\\', '/')) + '/locale/'
=======
        locale_path = os.path.dirname(os.path.abspath(_thisfile).replace('\\', '/')) + '/locale/'

        # Load locale file.
>>>>>>> origin/master

        try:
            with open(locale_path + 'locale.txt', 'r') as f:
                locale_code = f.read().rstrip('\n')
                if not locale_code:
                    first_run = True
                f.close()

        except FileNotFoundError:
            first_run = True


        if not first_run:

            if not os.path.isfile(locale_path + locale_code + '.json'):
                print('Locale with given language code doesn\'t exist. Fallback to English...')
                locale_code = 'English'

            with open(locale_path + locale_code + '.json', 'r') as f:
                self.locale = json.load(f)
                f.close()
        
        else:

            def set_settings(lang, setup_window):

                if lang == 'Select a language':
                    return

                if lang == 'Select a language':
                    return

                with open(locale_path + lang + '.json', 'r') as f:
                    self.locale = json.load(f)
                    f.close()

                with open(locale_path + 'locale.txt', 'w') as f:
                    f.write(lang)
                    f.close()
                
                setup_window.destroy()


            raw_languages_list = sorted(os.listdir(locale_path))
            languages_list = []

            for lang in raw_languages_list:
                if lang.endswith('.json'):
                    languages_list.append(lang[:-5])

            first_run_setup = tkinter.Tk()
            first_run_setup.geometry('300x180')
            first_run_setup.title('Jpegzilla - First run setup')
            first_run_setup.resizable(False, False)
            self._icon = tkinter.PhotoImage(file=JZ_ICON_TKINTER)
            first_run_setup.tk.call('wm', 'iconphoto', first_run_setup._w, self._icon)
            first_run_setup.configure(bg=self.bg)
            first_run_setup.protocol('WM_DELETE_WINDOW', lambda:sys.exit())

            language = tkinter.StringVar(first_run_setup)
            language.set('Select a language')

            first_run_setup_skip = tkinter.Button(
                    first_run_setup,
                    text='Skip setup (Will use defaults)',
                    relief='flat',
                    bg=self.bg,
                    fg=self.fg,
<<<<<<< HEAD
                    command=lambda:set_language('English', first_run_setup)
=======
                    command=lambda:set_settings('English', first_run_setup)
>>>>>>> origin/master
                    )
            first_run_setup_done = tkinter.Button(
                    first_run_setup,
                    text='Accept settings',
                    relief='flat',
                    bg=self.bg,
                    fg=self.fg,
                    command=lambda:set_settings(language.get(), first_run_setup)
                    )
            first_run_setup_lang = tkinter.OptionMenu(first_run_setup, language, *languages_list)
            first_run_setup_text = tkinter.Label(
                    first_run_setup,
                    bg=self.bg,
                    fg=self.fg,
                    text='Thanks for using Jpegzilla!\nPlease choose a language you wanna use\nor click "SKIP".\n'
                    )

            first_run_setup_text.pack()
            first_run_setup_lang.pack()
            first_run_setup_skip.pack(fill='x', side='bottom')
            first_run_setup_done.pack(fill='x', side='bottom')

            first_run_setup.mainloop()

        # Check if Mozjpeg is available.
        if OS == 'Windows':

            win_paths = os.getenv('PATH').split(';')

            if os.path.isfile('./cjpeg.exe'):
                print(self.locale['mozjpeg-found-local-dir'])
                if not glob.glob('./libjpeg-*.dll'):
                    messagebox.showerror(self.locale['title-error'], self.locale['mozjpeg-dll-missing-error'])
                pass

            elif os.path.isfile('./jpegzilla-mozjpeg_in_path'):
                pass

            else:

                print(self.locale['mozjpeg-search-in-path'])
                mozjpeg_found = False

                for path in win_paths:
                    path = path.replace('\\', '/') + ('/' if path[-1:] == '' else '')
                    if os.path.isfile(path + 'cjpeg.exe' ) and os.path.isfile(path + 'jpegtran.exe'):
                        print(self.locale['mozjpeg-found-path'].format(path=path))
                        mozjpeg_found = True
                        f = open('./jpegzilla-mozjpeg_in_path', 'w')
                        f.write(path)
                        f.close()
                        break

                if not mozjpeg_found:
                    print(self.locale['mozjpeg-not-found-error'])
                    messagebox.showerror(self.locale['title-error'], self.locale['mozjpeg-not-found-error'])
                    sys.exit()



        else:

            if not os.path.isfile('/usr/bin/cjpeg') and not os.path.isfile('/opt/mozjpeg/cjpeg'):
                print(self.locale['mozjpeg-not-found-error'])
                messagebox.showerror(self.locale['title-error'], self.locale['mozjpeg-not-found-error'])
                sys.exit()

        self.cancel_thread = False

        # Create root window.
        self.root = tkinter.Tk()
        self.root.geometry('780x550')
        self.root.title(self.locale['window-title'])
        self.root.resizable(False, False)
        self.root.configure(background=self.bg)
        self._icon = tkinter.PhotoImage(file=JZ_ICON_TKINTER)
        self.root.tk.call('wm', 'iconphoto', self.root._w, self._icon)

        # Primary buttons

        self.buttons = {
                    'run': tkinter.Button(
                        self.root, 
                        text=self.locale['run-button'], 
                        state='disabled', 
                        bg=self.bg, 
                        fg=self.fg, 
                        bd=0, 
                        disabledforeground=self.fgdis, 
                        highlightbackground=self.bg, 
                        highlightthickness=0, 
                        relief='flat', 
                        overrelief='flat',
                        font='Arial 10 bold',
                        command=lambda:self.run()
                        ),
                    'save': tkinter.Button(
                        self.root, 
                        text=self.locale['save-button'], 
                        state='disabled', 
                        bg=self.bg, 
                        fg=self.fg, 
                        bd=0, 
                        disabledforeground=self.fgdis, 
                        highlightbackground=self.bg, 
                        highlightthickness=0, 
                        relief='flat', 
                        overrelief='flat',
                        font='Arial 10 bold',
                        command=lambda:self.save_all()
                        ),
                    'help': tkinter.Button(
                        self.root, 
                        text=self.locale['help-button'], 
                        background=self.bg, 
                        fg=self.fg, 
                        bd=0, 
                        disabledforeground=self.fgdis, 
                        highlightbackground=self.bg, 
                        highlightthickness=0, 
                        relief='flat', 
                        overrelief='flat',
                        font='Arial 10 bold',
                        command=lambda:webbrowser.open_new(DOCS_URL)
                        ),
                    'import': tkinter.Button(
                        self.root, 
                        text=self.locale['import-button'], 
                        background=self.bg, 
                        fg=self.fg, 
                        bd=0, 
                        disabledforeground=self.fgdis, 
                        highlightbackground=self.bg, 
                        highlightthickness=0, 
                        relief='flat', 
                        overrelief='flat',
                        font='Arial 10 bold',
                        command=lambda:self.select_files()
                        )
                }

        dpos = [35, 10] # x, y

        for _, button in self.buttons.items():
            button.place(x=dpos[0], y=dpos[1])
            dpos[0] += 210

        # Parameters/Options

        self.cjpeg_parameters = {
                '-quality': tkinter.IntVar(),
                '-smooth': tkinter.IntVar(),
                '-progressive': tkinter.IntVar(),
                '-greyscale': tkinter.IntVar(),
                '-arithmetic': tkinter.IntVar(),
                '-colorformat': tkinter.StringVar(self.root),
                '-optimize': tkinter.IntVar(),
                '-baseline': tkinter.IntVar(),
                '-notrellis': tkinter.IntVar()
                }

        self.jpegtran_parameters = {
            '-rotate': tkinter.StringVar(self.root, value='0\N{DEGREE SIGN}'),
            '-transpose': tkinter.IntVar(),
            '-transverse': tkinter.IntVar(),
            '-trim': tkinter.IntVar(),
            '-crop': tkinter.StringVar(self.root)
        }

        self.cjpeg_parameters['-colorformat'].set('YUV 4:2:0')
        def uncheck_progressive():
            if self.cjpeg_parameters['-progressive'].get() or self.gui_options['progressive']['state'] == 'normal':
                self.cjpeg_parameters['-progressive'].set(0)
                self.gui_options['progressive'].configure(state='disabled')
            else:
                self.gui_options['progressive'].configure(state='normal')


        def switch_checked(parameter, parameter_group):

            if parameter_group == 'cjpeg':
                if self.cjpeg_parameters[parameter].get() or self.gui_options[parameter[1:]]['state'] == 'normal':
                    self.cjpeg_parameters[parameter].set(0)
                    self.gui_options[parameter[1:]].configure(state='disabled')
                else:
                    self.gui_options[parameter[1:]].configure(state='normal')

            elif parameter_group == 'jpegtran':
                if self.jpegtran_parameters[parameter].get() or self.gui_options[parameter[1:]]['state'] == 'normal':
                    self.jpegtran_parameters[parameter].set(0)
                    self.gui_options[parameter[1:]].configure(state='disabled')
                else:
                    self.gui_options[parameter[1:]].configure(state='normal')


        self.gui_options = {
                'quality': tkinter.Scale(
                    self.root, label=self.locale['image-quality'], orient='horizontal', length='200', 
                    bg=self.bg, fg=self.fg, 
                    bd=0, 
                    highlightbackground=self.bg, 
                    highlightthickness=0, 
                    relief='flat', 
                    variable=self.cjpeg_parameters['-quality']
                    ),
                'smoothing': tkinter.Scale(
                    self.root, label=self.locale['smoothing'], orient='horizontal', length='200', 
                    bg=self.bg, fg=self.fg, 
                    bd=0, 
                    highlightbackground=self.bg, 
                    highlightthickness=0, 
                    relief='flat', 
                    variable=self.cjpeg_parameters['-smooth']
                    ),
                'progressive': tkinter.Checkbutton(
                    self.root, text=self.locale['progressive'],
                    bg=self.bg, fg=self.fg,
                    bd=0, 
                    highlightbackground=self.bg, 
                    highlightthickness=0, 
                    relief='flat', 
                    variable=self.cjpeg_parameters['-progressive']
                    ),
                'greyscale': tkinter.Checkbutton(
                    self.root, text=self.locale['greyscale'], 
                    bg=self.bg, fg=self.fg,
                    bd=0, 
                    highlightbackground=self.bg, 
                    highlightthickness=0, 
                    relief='flat', 
                    variable=self.cjpeg_parameters['-greyscale']
                    ),
                'arithmetic': tkinter.Checkbutton(
                    self.root, text=self.locale['arithmetic'], 
                    bg=self.bg, fg=self.fg,
                    bd=0, 
                    highlightbackground=self.bg, 
                    highlightthickness=0, 
                    relief='flat', 
                    variable=self.cjpeg_parameters['-arithmetic'],
                    command=lambda:switch_checked('-optimize', 'cjpeg')
                    ),
                'colorformat': tkinter.OptionMenu(
                    self.root, 
                    self.cjpeg_parameters['-colorformat'], *['YUV 4:2:0', 'YUV 4:2:2', 'YUV 4:4:4', 'RGB']
                    ),
                'optimize': tkinter.Checkbutton(
                    self.root, text=self.locale['optimize'],
                    bg=self.bg, fg=self.fg,
                    bd=0,
                    highlightbackground=self.bg,
                    highlightthickness=0,
                    relief='flat',
                    variable=self.cjpeg_parameters['-optimize'],
                    ),
                 'baseline': tkinter.Checkbutton(
                    self.root, text=self.locale['baseline'],
                    bg=self.bg, fg=self.fg,
                    bd=0,
                    highlightbackground=self.bg,
                    highlightthickness=0,
                    relief='flat',
                    variable=self.cjpeg_parameters['-baseline'],
<<<<<<< HEAD
                    command=lambda:uncheck_progressive()
=======
                    command=lambda:switch_checked('-progressive', 'cjpeg')
>>>>>>> origin/master
                    ),
                 'notrellis': tkinter.Checkbutton(
                    self.root, text=self.locale['notrellis'],
                    bg=self.bg, fg=self.fg,
                    bd=0,
                    highlightbackground=self.fg,
                    highlightthickness=0,
                    relief='flat',
                    variable=self.cjpeg_parameters['-notrellis']
<<<<<<< HEAD
                    )
=======
                    ),

                 'rotate': tkinter.OptionMenu(
                    self.root,
                    self.jpegtran_parameters['-rotate'],
                    *['0\N{DEGREE SIGN}', '90\N{DEGREE SIGN}', '180\N{DEGREE SIGN}', '270\N{DEGREE SIGN}']
                 ),
                 'transpose': tkinter.Checkbutton(
                    self.root, text=self.locale['transpose'],
                    bg=self.bg, fg=self.fg,
                    bd=0,
                    highlightbackground=self.fg,
                    highlightthickness=0,
                    relief='flat',
                    variable=self.jpegtran_parameters['-transpose'],
                    command=lambda:switch_checked('-transverse', 'jpegtran')
                 ),
                 'transverse': tkinter.Checkbutton(
                    self.root, text=self.locale['transverse'],
                    bg=self.bg, fg=self.fg,
                    bd=0,
                    highlightbackground=self.fg,
                    highlightthickness=0,
                    relief='flat',
                    variable=self.jpegtran_parameters['-transverse'],
                    command=lambda:switch_checked('-transpose', 'jpegtran')
                 ),
                 'trim': tkinter.Checkbutton(
                    self.root, text=self.locale['trim'],
                    bg=self.bg, fg=self.fg,
                    bd=0,
                    highlightbackground=self.fg,
                    highlightthickness=0,
                    relief='flat',
                    variable=self.jpegtran_parameters['-trim']
                 ),
                 'crop': tkinter.Entry(
                    self.root,
                    width='24',
                    bg='#8E8E8E', fg='#FFFFFF',
                    bd=0,
                    highlightbackground=self.fg,
                    highlightthickness=0,
                    relief='flat',
                    textvariable=self.jpegtran_parameters['-crop'],
                 ),
>>>>>>> origin/master
                }

        # - Labels
        rotate_label = tkinter.Label(self.root, bg=self.bg, fg=self.fg, text=self.locale['rotate'])
        crop_label = tkinter.Label(self.root, bg=self.bg, fg=self.fg, text=self.locale['crop'])

        # - Set the defaults
        self.gui_options['progressive'].select()
<<<<<<< HEAD
        self.gui_options['quality'].set(90)
=======
        self.gui_options['quality'].set(75)
>>>>>>> origin/master
        self.gui_options['optimize'].select()

        # - Place items
        self.gui_options['quality'].place(x=10, y=45)
        self.gui_options['smoothing'].place(x=10, y=105)
        self.gui_options['progressive'].place(x=220, y=70)
        self.gui_options['greyscale'].place(x=220, y=90)
        self.gui_options['arithmetic'].place(x=220, y=110)
        self.gui_options['colorformat'].place(x=225, y=130)
        self.gui_options['optimize'].place(x=400, y=70)
        self.gui_options['baseline'].place(x=400, y=90)
        self.gui_options['notrellis'].place(x=400, y=125)
<<<<<<< HEAD
=======

        rotate_label.place(x=13, y=170)
        self.gui_options['rotate'].place(x=15, y=190)
        self.gui_options['transpose'].place(x=10, y=225)
        self.gui_options['transverse'].place(x=10, y=245)
        self.gui_options['trim'].place(x=170, y=180)
        crop_label.place(x=183, y=205)
        self.gui_options['crop'].place(x=185, y=240)
>>>>>>> origin/master

        # Queue/List

        self.queue = tkinter.Frame(self.root, bg=self.bg)
        self.queue.pack(side='bottom')

        self.file_queue_rmdone = tkinter.Button(
                self.queue,
                text=self.locale['clear-all-button'], 
                bg=self.bg, 
                fg=self.fg, 
                bd=0, 
                disabledforeground=self.fgdis, 
                highlightbackground=self.bg, 
                highlightthickness=0, 
                relief='flat', 
                overrelief='flat',
                font='Arial 9 bold',
                command=lambda:self.clean()
                )
        self.file_queue_rmdone.pack(side='top', anchor='e')

        self.cancel_button = tkinter.Button(
                self.queue,
                text=self.locale['cancel-button'],
                state='disabled',
                bg=self.bg,
                fg=self.fg,
                bd=0,
                disabledforeground=self.fgdis,
                highlightbackground=self.bg,
                highlightthickness=0,
                relief='flat',
                overrelief='flat',
                font='Arial 9 bold',
                command=lambda:self.cancel()
                )
        self.cancel_button.pack(side='top', anchor='e')

        self.queue_label = tkinter.Label(self.queue, bg=self.bg, fg=self.fg, text=self.locale['loaded-files'].format('0'))
        self.queue_label.pack(side='top', anchor='w')

        self.file_queue = tkinter.ttk.Treeview(self.queue, selectmode='browse')
        self.file_queue['columns'] = ('size', 'status', 'loc')
        self.file_queue.heading('#0', text=self.locale['treeview-filename'])
        self.file_queue.column('#0', width=345, stretch='no')
        self.file_queue.heading('size', text=self.locale['treeview-size'])
        self.file_queue.column('size', width=245, stretch='no')
        self.file_queue.heading('status', text=self.locale['treeview-status'])
        self.file_queue.column('status', width=195, stretch='no')
        self.file_queue.heading('loc')
        self.file_queue.column('loc', width=0, stretch='no')
        self.file_queue.pack(side='left')

        self.file_queue_vsb = tkinter.ttk.Scrollbar(self.queue, orient='vertical', command=self.file_queue.yview)
        self.file_queue_vsb.pack(side='right', fill='y')

        self.file_queue.configure(yscrollcommand=self.file_queue_vsb.set)

        self.file_queue.bind('<Delete>', lambda x:self.remove_files())
        self.file_queue.bind('<Return>', lambda x:self.show_preview())
        self.file_queue.bind('<Double-Button-1>', lambda x:self.show_preview())

        self.root.mainloop()

    def remove_files(self):

        selected_files = self.file_queue.selection()
        for image in selected_files:
            self.file_queue.delete(image)

        self.queue_label.configure(text=self.locale['loaded-files'].format(
            str(len(
                self.file_queue.get_children()
                ))
            ))
        if not len(self.file_queue.get_children()):
            self.buttons['run'].config(state='disabled')


    def show_preview(self):
    
        selected_file = self.file_queue.item(self.file_queue.selection())['values']
        try:
            file_name = ntpath.basename(selected_file[2])
        except IndexError:
            return
<<<<<<< HEAD

        self.preview_window = tkinter.Toplevel(self.root)
        self.preview_window.title(self.locale['image-preview-title'].format(filename=file_name))
=======

        # 'status'
        if selected_file[1] == self.locale['status-error']:
            return

        self.preview_window = tkinter.Toplevel(self.root)
        self.preview_window.title(self.locale['image-preview-title'].format(filename=file_name))

        location = ((TEMPDIR + file_name) if (selected_file[1] == self.locale['status-completed']) else selected_file[2])

        if OS == 'Windows':
            command = ['start', location.replace('/', "\\")]
        else:
            command = ['xdg-open', location]
>>>>>>> origin/master

        oiiv_button = tkinter.Button(
                self.preview_window,
                width='600',
                text=self.locale['open-in-image-viewer'],
                command=lambda:subprocess.Popen(command, shell=(OS == 'Windows'))
                )
        oiiv_button.pack()

        self.preview_imgfile = Image.open( TEMPDIR + file_name if selected_file[1] == self.locale['status-completed'] else selected_file[2] )

        required_width = 800
        wpercent = (required_width / float(self.preview_imgfile.size[0]) )
        hsize = int( (float(self.preview_imgfile.size[1]) * float(wpercent)) )
        self.preview_imgfile = self.preview_imgfile.resize((required_width, hsize), Image.ANTIALIAS)

        self.preview_image = ImageTk.PhotoImage(self.preview_imgfile)

        self.preview = tkinter.Label(self.preview_window, image=self.preview_image)
        self.preview.image = self.preview_image
        self.preview.pack(fill='both', expand='yes')

    def clean(self):

        all_files = self.file_queue.get_children()
        for image in all_files:
            self.file_queue.delete(image)

        self.queue_label.configure(text=self.locale['loaded-files'].format('0'))
        self.buttons['run'].configure(state='disabled')
        self.buttons['save'].configure(state='disabled')

    def save_all(self):

        location = tkinter.filedialog.askdirectory(title=self.locale['save-all-title'], initialdir='~')

        compressed_images = self.file_queue.get_children()

        for image in compressed_images:
            child_data = self.file_queue.item(image)['values']
            filename = ntpath.basename(child_data[2])
            if child_data[1] == self.locale['status-completed']:
                shutil.move(TEMPDIR + filename, location + '/' + filename)


    def select_files(self):

        filenames = tkinter.filedialog.askopenfilenames(
                    initialdir='~',
                    title=self.locale['select-files-title'],
                    filetypes=(
                        (self.locale['select-filetypes']['compatible-formats'], ['*.jpeg', '*.jpg', '*.tga']),
                        (self.locale['select-filetypes']['all-files'], '*.*')
                    )
                )
        self.filenames = self.root.tk.splitlist(filenames)

        files_already_imported = {}
        ids_already_imported = self.file_queue.get_children()
        for node in ids_already_imported:
            files_already_imported[self.file_queue.item(node)['text']] = self.file_queue.item(node)['values'][1]
        
        print(files_already_imported) if self.debug else None

        for image in self.filenames:
 
            basename = ntpath.basename(image)

            if (not basename in files_already_imported.keys()) or (not files_already_imported[basename] == self.locale['status-new']):
                filesize = self.convert_size(os.stat(image).st_size)

                self.file_queue.insert('', 'end', text=basename, values=(
                         filesize, self.locale['status-new'], image
                    ))
            
            else:
                messagebox.showerror(self.locale['title-error'], self.locale['import-same-file'].format(filename=basename))

        if self.filenames:
            self.buttons['run'].config(state='normal')

        self.queue_label.configure(text=self.locale['loaded-files'].format(str(len(self.file_queue.get_children()))))

    def run(self):

        self.compress_thread = threading.Thread(target=self.compress)
        self.compress_thread.start()

    def cancel(self):
        self.cancel_thread = True

    def compress(self):

        self.buttons['run'].configure(state='disabled')
        self.cancel_button.configure(state='normal')

        command = "cjpeg {targa} -outfile {filename}"
        jpegtran_command = "jpegtran"

        # CJPEG

        for parameter, value in self.cjpeg_parameters.items():
            value = value.get()
            if (not parameter in ['-quality', '-smooth', '-colorformat']):
                if value:
                    command += (" {0} {1}".format(parameter, ('' if value in [0, 1] else value)))
                    jpegtran_command += (' -arithmetic' if parameter == '-arithmetic' else '')

            elif parameter == '-colorformat':
                if value == 'RGB':
                    command += '-rgb'
                elif value == 'YUV 4:2:0':
                    command += '-sample 2x2'
                elif value == 'YUV 4:2:2':
                    command += '-sample 2x1'
                elif value == 'YUV 4:4:4':
                    command += '-sample 1x1'

            else:
                command += ' {0} {1}'.format(parameter, value)

        # JPEGTRAN

        for parameter, value in self.jpegtran_parameters.items():
            value = value.get()
            if (not parameter in ['-rotate', '-crop']):
                if value:
                    jpegtran_command += (" {0} {1}".format(parameter, ('' if value in [0, 1] else value)))

            elif parameter == '-rotate':
                value = value[:-1] # remove degree character
                try:
                    if int(value) > 360:
                        raise ValueError
                    elif int(value) == 0:
                        pass
                    else:
                        jpegtran_command += ' -rotate ' + value
                except ValueError: # not number or higher than 360 degrees
                    pass

            elif parameter == '-crop':
                # ^ - start of the string
                # \d+ - digits of unlimited length
                # x - just "x"
                # \+ - just "+"
                reg_match = re.fullmatch(r'^\d+x\d+\+\d+\+\d+$', value)
                if reg_match == None:
                    pass
                else:
                    jpegtran_command += ' -crop ' + value

            else:
                jpegtran_command += (' {0} {1}'.format(parameter, ('' if value in [0, 1] else value)))

        files_to_compress = self.file_queue.get_children()

        for entry in files_to_compress:

            entry_data = self.file_queue.item(entry)['values']
            img, extension = os.path.splitext(entry_data[2])
            img = img.split('/')[len(img.split('/')) - 1]

            if entry_data[1] in [self.locale['status-completed'], self.locale['status-error']]:
                pass
            
            else:

                self.file_queue.item(entry, values=( entry_data[0], self.locale['status-running'], entry_data[2] ))

                tmp_file_name = (TEMPDIR + img + extension)
                counter = 1

                while os.path.isfile(tmp_file_name):
                    counter += 1
                    tmp_file_name = (TEMPDIR + img + str(counter) + extension)

                cjpegc = (command.format(filename=tmp_file_name, targa=('-targa' if extension == '.tga' else '')) + ' ' + entry_data[2])
                jpegtranc = (jpegtran_command + ' -outfile ' + tmp_file_name + ' ' + tmp_file_name)

                if self.debug:
                    print(cjpegc)
                    print(jpegtranc)
                    print(entry_data)

                subprocess.Popen(cjpegc, shell=True, stdout=subprocess.PIPE).wait()
                subprocess.Popen(jpegtranc, shell=True, stdout=subprocess.PIPE).wait()

                new_size = self.convert_size(os.stat(TEMPDIR + img + extension).st_size)
                status = (self.locale['status-completed'] if not new_size == '0B' else self.locale['status-error'])

<<<<<<< HEAD
                if self.debug:
                    print(c)

                subprocess.Popen(c, shell=True, stdout=subprocess.PIPE).wait()
                self.file_queue.item(entry, values=( entry_data[0] + ' -> ' + hurry.filesize.size(os.stat(TEMPDIR + img + extension).st_size), self.locale['status-completed'], entry_data[2] ))
=======
                self.file_queue.item(
                        entry, 
                        values=( 
                            entry_data[0] + ' -> ' + new_size,
                            status,
                            tmp_file_name
                            )
                        )
>>>>>>> origin/master

            if self.cancel_thread:
                self.cancel_thread = False
                break

        self.buttons['run'].configure(state='normal')
        self.buttons['save'].configure(state='normal')
        self.cancel_button.configure(state='disabled')

    def convert_size(self, size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])

if __name__ == '__main__':
    
    try:
        if sys.argv[1].startswith('-'):

            if sys.argv[1] in ['-v', '--version']:

                print("Jpegzilla {}\nhttps://github.com/fabulouskana/jpegzilla".format(VER))

            elif sys.argv[1] in ['-h', '--help']:

                print("Run program by just typing \"jpegzilla\" or by running script without any arguments.")
                print("      -v, --version  - Display version information.")

            else:

                print("Unknown argument. Type --help for more information.")

            sys.exit()

        else:
            raise IndexError

    except IndexError:
        pass

    jz = jpegzilla()

