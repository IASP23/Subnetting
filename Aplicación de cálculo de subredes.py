import tkinter as tk
import tkinter.font as tkFont
import ipaddress
from tkinter import ttk

# APLICACION QUE CALCULE EL NUMERO DE SUBREDES DE UNA IP, ADEMAS VERIFIQUE EL ANGO DE IPS VALIDAS
# PARA CADA SUB-RED Y SU BROADCAST


class App:
    def __init__(self, root):
        # setting title
        root.title("SubNetting")
        # setting window size
        width = 750
        height = 400
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height,
                                    (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        btn_cal_redes = tk.Button(root)
        btn_cal_redes["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times', size=10)
        btn_cal_redes["font"] = ft
        btn_cal_redes["fg"] = "#000000"
        btn_cal_redes["justify"] = "center"
        btn_cal_redes["text"] = "Calcular por Host"
        btn_cal_redes.place(x=450, y=70, width=120, height=52)
        btn_cal_redes["command"] = self.calcular_subredes_host

        btn_cal_redes = tk.Button(root)
        btn_cal_redes["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times', size=10)
        btn_cal_redes["font"] = ft
        btn_cal_redes["fg"] = "#000000"
        btn_cal_redes["justify"] = "center"
        btn_cal_redes["text"] = "Calcular por Subredes"
        btn_cal_redes.place(x=570, y=70, width=130, height=52)
        btn_cal_redes["command"] =  self.calcular_subredes_subredes

        titulo = tk.Label(root)
        ft = tkFont.Font(family='Times', size=10)
        titulo["font"] = ft
        titulo["fg"] = "#333333"
        titulo["justify"] = "center"
        titulo["text"] = "CALCULADORA DE SUBREDES"
        titulo.place(x=260, y=20, width=189, height=31)

        GLabel_220 = tk.Label(root)
        ft = tkFont.Font(family='Times', size=10)
        GLabel_220["font"] = ft
        GLabel_220["fg"] = "#333333"
        GLabel_220["justify"] = "center"
        GLabel_220["text"] = "Direccion IP y mascara de subred:"
        GLabel_220.place(x=28, y=70,  height=25)

        GLabel_222 = tk.Label(root)
        ft = tkFont.Font(family='Times', size=10)
        GLabel_222["font"] = ft
        GLabel_222["fg"] = "#333333"
        GLabel_222["justify"] = "center"
        GLabel_222["text"] = "(192.168.10.0 / 24):"
        GLabel_222.place(x=160, y=45,  height=25)

        label_ip_validas = tk.Label(root)
        ft = tkFont.Font(family='Times', size=10)
        label_ip_validas["font"] = ft
        label_ip_validas["fg"] = "#333333"
        label_ip_validas["justify"] = "center"
        label_ip_validas["text"] = "IP's validas: "
        label_ip_validas.place(x=290, y=70, width=70, height=25)

        label_subredes = tk.Label(root)
        ft = tkFont.Font(family='Times', size=10)
        label_subredes["font"] = ft
        label_subredes["fg"] = "#333333"
        label_subredes["justify"] = "center"
        label_subredes["text"] = "Subredes: "
        label_subredes.place(x=290, y=110, width=70, height=25)

        GLabel_161 = tk.Label(root)
        ft = tkFont.Font(family='Times', size=10)
        GLabel_161["font"] = ft
        GLabel_161["fg"] = "#333333"
        GLabel_161["justify"] = "center"
        GLabel_161["text"] = "Mascara de Subred: "
        GLabel_161.place(x=20, y=110, width=130, height=30)


    def reset_table(self, tabla):
        if tabla.get_children(): # Verificar si la tabla no está vacía
                for row in tabla.get_children(): # Iterar sobre las filas existentes
                    tabla.delete(row) # Eliminar cada fila de la tabla

    def calcular_subredes_host(self):
        try:
            app.reset_table(tabla)

            direccion_ip = ipaddress.IPv4Network(direccion_ip_txt.get())
            num_host = int(num_host_txt.get())

            # Calculamos la máscara de subred necesaria para el número de subredes solicitado 32-5
            mascara_bits = direccion_ip.max_prefixlen - \
                (num_host - 1).bit_length()

            # Creamos una lista vacía para almacenar las subredes
            subredes = []
            # 
            max256 = 8 - (num_host - 1).bit_length() 
            n_sub = 2**max256 

            for i in range(n_sub):
                subred = ipaddress.IPv4Network(
                    (direccion_ip.network_address + i * 2**(32-mascara_bits), mascara_bits))
                subredes.append(subred)

            # Mostramos el rango de direcciones IP configurables para cada subred
            for i, subred in enumerate(subredes):

                primer_ip = list(subred.hosts())[0]
                ultima_ip = list(subred.hosts())[-1]
                rango_ip = f"{primer_ip} - {ultima_ip}"

                tabla.insert("", tk.END, values=(
                    i+1, subred, rango_ip, subred.broadcast_address))
                tabla.place(x=30, y=140, width=672, height=225)

                ip_with_mask = direccion_ip.with_prefixlen

            mascara_sub_txt.config(text=ip_with_mask)

        except ValueError:
            mascara_sub_txt.config(text="Error")

    def calcular_subredes_subredes(self):      
        try:
            app.reset_table(tabla)
            direccion_ip = ipaddress.IPv4Network(direccion_ip_txt.get())
            num_sub = int(num_subredes_txt.get())

            # Calcular la cantidad de bits necesarios para el número de subredes especificado
            bits_necesarios = (num_sub - 1).bit_length()

            # Crear una lista de objetos de dirección de red para las subredes
            subredes = list(direccion_ip.subnets(prefixlen_diff=bits_necesarios))

            for i, subnet in enumerate(subredes):
                primer_ip = list(subnet.hosts())[0]
                ultima_ip = list(subnet.hosts())[-1]
                rango_ip = f"{primer_ip} - {ultima_ip}"

                tabla.insert("", tk.END, values=(
                    i+1, subnet, rango_ip, subnet.broadcast_address))
                tabla.place(x=30, y=140, width=672, height=225)

        except ValueError:
            mascara_sub_txt.config(text="Error")



if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)

    # Entrada de datos

    direccion_ip_txt = tk.Entry(root)
    direccion_ip_txt["borderwidth"] = "1px"
    ft = tkFont.Font(family='Times', size=10)
    direccion_ip_txt["font"] = ft
    direccion_ip_txt["fg"] = "#333333"
    direccion_ip_txt["justify"] = "center"
    direccion_ip_txt["text"] = "direccion_ip_txt"
    direccion_ip_txt.pack()
    direccion_ip_txt.place(x=150, y=70, width=119, height=30)

    num_host_txt = tk.Entry(root)
    num_host_txt["borderwidth"] = "1px"
    ft = tkFont.Font(family='Times', size=10)
    num_host_txt["font"] = ft
    num_host_txt["fg"] = "#333333"
    num_host_txt["justify"] = "center"
    num_host_txt["text"] = "num_host_txt"
    num_host_txt.place(x=360, y=70, width=70, height=25)

    num_subredes_txt = tk.Entry(root)
    num_subredes_txt["borderwidth"] = "1px"
    ft = tkFont.Font(family='Times', size=10)
    num_subredes_txt["font"] = ft
    num_subredes_txt["fg"] = "#333333"
    num_subredes_txt["justify"] = "center"
    num_subredes_txt["text"] = "num_subredes_txt"
    num_subredes_txt.place(x=360, y=110, width=70, height=25)


    # Tabla
    tabla = ttk.Treeview(root, columns=(
        "N", "Subred", "Rango de IPs", "Broadcast"), show="headings")
    ft = tkFont.Font(family='Times', size=15)
    tabla.place(x=30, y=140, width=672, height=225)

    tabla.heading("N", text="N")
    tabla.heading("Subred", text="Subred")
    tabla.heading("Rango de IPs", text="Rango de IPs")
    tabla.heading("Broadcast", text="Broadcast")

    tabla.column("N", width=15, anchor="center")
    tabla.column("Subred", anchor="center")
    tabla.column("Rango de IPs", anchor="center")
    tabla.column("Broadcast", anchor="center")

    # Mascara de Subred
    mascara_sub_txt = tk.Label(root)
    ft = tkFont.Font(family='Times', size=10)
    mascara_sub_txt["font"] = ft
    mascara_sub_txt["fg"] = "#333333"
    mascara_sub_txt["text"] = "----------"
    mascara_sub_txt.place(x=170, y=110, width=120, height=25)




    root.mainloop()
