import os
import re

def clean_conditionals(directory):
    # Map of filename -> list of regex patterns to remove from END of file
    remove_from_end = {
        '03_introducción_a_java.tex': [r'\\ifruby'],
        '04_introducción_a_ruby.tex': [r'\\ifpython'],
        '05_introducción_a_python.tex': [r'\\ifcsharp'],
        '06_introducción_a_c.tex': [r'\\ifscala'],
        '07_introducción_a_scala.tex': [r'\\ifd'],
        '14_objetos_constantes.tex': [r'\\ifcpp'],
        '24_afirmaciones.tex': [r'\\ifdraft'],
        '26_pruebas_de_unidad.tex': [r'\\ifjava'],
        '27_multihilos_introducción_a_la_programación_concurrente_en_java.tex': [r'\\ifjava'],
        '28_multihilos_programación_concurrente_en_java_2.tex': [r'\\ifpython'],
        '29_multihilos_en_python.tex': [r'\\ifjava'],
        '30_java_clases_anidadas_y_anónimas.tex': [r'\\ifjava'],
        '31_java_expresiones_lambda_lambda.tex': [r'\\ifjava'],
        '32_java_interfaz_gráfica_con_javafx.tex': [r'\\ifjava'],
        '33_java_manejo_de_eventos_con_javafx.tex': [r'\\ifjava'],
        '34_programación_en_red_con_java.tex': [r'\\ifjava'],
        '37_apéndice_a_herramientas_adicionales_sugeridas.tex': [r'\\ifdraft'],
    }

    # Map of filename -> list of regex patterns to remove from START of file
    remove_from_start = {
        '26_pruebas_de_unidad.tex': [r'\\fi'],
    }

    # Process removals from end
    for filename, patterns in remove_from_end.items():
        filepath = os.path.join(directory, filename)
        if not os.path.exists(filepath): continue
        
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        # Check last few lines
        modified = False
        # Iterate backwards
        for i in range(len(lines)-1, max(-1, len(lines)-10), -1):
            line = lines[i].strip()
            for pattern in patterns:
                if re.search(pattern, line):
                    # Remove this line
                    lines.pop(i)
                    modified = True
                    break
        
        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            print(f"Cleaned end of {filename}")

    # Process removals from start
    for filename, patterns in remove_from_start.items():
        filepath = os.path.join(directory, filename)
        if not os.path.exists(filepath): continue
        
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        # Check first few lines
        modified = False
        for i in range(min(5, len(lines))):
            line = lines[i].strip()
            for pattern in patterns:
                if re.search(pattern, line):
                    # Remove this line
                    lines.pop(i)
                    modified = True
                    # Adjust index since we popped
                    i -= 1 
                    break
        
        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            print(f"Cleaned start of {filename}")

if __name__ == "__main__":
    clean_conditionals('capitulos')
