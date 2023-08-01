def create_html(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    html_output = '<html>\n<body>\n'

    for line in lines:

        try:    
            line = line.strip()  # Supprimer les espaces vides et sauts de ligne
            print(line)
            html_output += f'<p><a href="{line}" target="_blank">{line}</a></p>\n'

            html_output += '</body>\n</html>'

            with open('output.html', 'w',encoding='ascii') as file:
                file.write(html_output)

        except ValueError:
            print("error")


create_html(r'C:\Users\CAML078995\Documents\Python\ExplorateurDeFichier\allfiles.txt')


