import pandas as pd
import openpyxl
from pathlib import Path
import json
import sys
import os

# Añadir directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.base_module import BaseModule

class ExcelModule(BaseModule):
    """Módulo para trabajar con archivos Excel."""
    
    def __init__(self):
        """Inicializa el módulo de Excel."""
        super().__init__("excel")
    
    def _get_capabilities(self):
        """
        Devuelve las capacidades del módulo de Excel.
        
        Returns:
            list: Lista de capacidades
        """
        return [
            "read_excel",
            "write_excel",
            "merge_excel_files",
            "extract_data",
            "apply_formula",
            "create_pivot_table",
            "generate_chart",
            "filter_data"
        ]
    
    def read_excel(self, file_path, sheet_name=0, header=0):
        """
        Lee datos de un archivo Excel.
        
        Args:
            file_path (str): Ruta al archivo Excel
            sheet_name (str/int, optional): Nombre o índice de la hoja
            header (int, optional): Fila de cabecera
            
        Returns:
            dict: Datos leídos del archivo Excel
        """
        try:
            # Verificar que el archivo existe
            file = Path(file_path)
            if not file.exists():
                return {"success": False, "error": f"El archivo {file_path} no existe"}
            
            # Leer el archivo Excel
            df = pd.read_excel(file_path, sheet_name=sheet_name, header=header)
            
            # Convertir DataFrame a diccionario
            data = df.to_dict(orient='records')
            
            # Obtener nombres de columnas
            columns = df.columns.tolist()
            
            return {
                "success": True,
                "data": data,
                "columns": columns,
                "rows": len(data),
                "file_path": file_path,
                "sheet_name": sheet_name
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def write_excel(self, data, file_path, sheet_name="Sheet1", index=False):
        """
        Escribe datos en un archivo Excel.
        
        Args:
            data (dict/list): Datos a escribir
            file_path (str): Ruta donde guardar el archivo
            sheet_name (str, optional): Nombre de la hoja
            index (bool, optional): Incluir índice
            
        Returns:
            dict: Resultado de la operación
        """
        try:
            # Convertir datos a DataFrame
            if isinstance(data, list):
                df = pd.DataFrame(data)
            elif isinstance(data, dict):
                df = pd.DataFrame.from_dict(data, orient='index' if len(data) > 0 and isinstance(next(iter(data.values())), dict) else 'columns')
            else:
                return {"success": False, "error": "Formato de datos no soportado"}
            
            # Crear directorio si no existe
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Escribir DataFrame a Excel
            df.to_excel(file_path, sheet_name=sheet_name, index=index)
            
            return {
                "success": True,
                "file_path": file_path,
                "sheet_name": sheet_name,
                "rows": len(df),
                "columns": len(df.columns)
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def merge_excel_files(self, file_paths, output_path, sheet_name="Sheet1", how='outer'):
        """
        Combina múltiples archivos Excel en uno solo.
        
        Args:
            file_paths (list): Lista de rutas a los archivos Excel
            output_path (str): Ruta donde guardar el archivo combinado
            sheet_name (str, optional): Nombre de la hoja
            how (str, optional): Tipo de join ('outer', 'inner', etc.)
            
        Returns:
            dict: Resultado de la operación
        """
        try:
            # Verificar que todos los archivos existen
            missing_files = []
            for file_path in file_paths:
                if not Path(file_path).exists():
                    missing_files.append(file_path)
            
            if missing_files:
                return {"success": False, "error": f"Archivos no encontrados: {missing_files}"}
            
            # Leer y combinar los archivos
            dfs = []
            for file_path in file_paths:
                df = pd.read_excel(file_path)
                dfs.append(df)
            
            # Combinar DataFrames
            if how == 'concat':
                combined_df = pd.concat(dfs, ignore_index=True)
            else:
                # Para merge, necesitamos columnas en común
                # Por simplicidad, usamos concat en esta implementación
                combined_df = pd.concat(dfs, ignore_index=True)
            
            # Crear directorio si no existe
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Guardar DataFrame combinado
            combined_df.to_excel(output_path, sheet_name=sheet_name, index=False)
            
            return {
                "success": True,
                "file_path": output_path,
                "sheet_name": sheet_name,
                "rows": len(combined_df),
                "columns": len(combined_df.columns)
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def extract_data(self, file_path, query, sheet_name=0):
        """
        Extrae datos específicos de un archivo Excel usando una consulta.
        
        Args:
            file_path (str): Ruta al archivo Excel
            query (dict): Filtros y selecciones a aplicar
            sheet_name (str/int, optional): Nombre o índice de la hoja
            
        Returns:
            dict: Datos extraídos
        """
        try:
            # Verificar que el archivo existe
            if not Path(file_path).exists():
                return {"success": False, "error": f"Archivo no encontrado: {file_path}"}
            
            # Leer el archivo Excel
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            
            # Aplicar filtros si se especifican
            if "filters" in query:
                for column, value in query["filters"].items():
                    if column in df.columns:
                        if isinstance(value, list):
                            df = df[df[column].isin(value)]
                        else:
                            df = df[df[column] == value]
            
            # Seleccionar columnas si se especifican
            if "columns" in query and query["columns"]:
                valid_columns = [col for col in query["columns"] if col in df.columns]
                if valid_columns:
                    df = df[valid_columns]
            
            # Limitar número de filas si se especifica
            if "limit" in query and isinstance(query["limit"], int):
                df = df.head(query["limit"])
            
            # Convertir a registros
            data = df.to_dict(orient='records')
            
            return {
                "success": True,
                "data": data,
                "rows": len(data),
                "columns": df.columns.tolist()
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def apply_formula(self, file_path, formulas, output_path=None, sheet_name=0):
        """
        Aplica fórmulas a un archivo Excel.
        
        Args:
            file_path (str): Ruta al archivo Excel
            formulas (list): Lista de fórmulas a aplicar
            output_path (str, optional): Ruta donde guardar el resultado
            sheet_name (str/int, optional): Nombre o índice de la hoja
            
        Returns:
            dict: Resultado de la operación
        """
        try:
            # Verificar que el archivo existe
            if not Path(file_path).exists():
                return {"success": False, "error": f"Archivo no encontrado: {file_path}"}
            
            # Si no se especifica salida, sobreescribir el original
            if not output_path:
                output_path = file_path
            
            # Abrir el archivo con openpyxl
            workbook = openpyxl.load_workbook(file_path)
            
            # Obtener la hoja
            if isinstance(sheet_name, int):
                sheet = workbook.worksheets[sheet_name]
            else:
                sheet = workbook[sheet_name]
            
            # Aplicar cada fórmula
            for formula in formulas:
                if "cell" in formula and "formula" in formula:
                    cell = formula["cell"]
                    formula_str = formula["formula"]
                    sheet[cell] = formula_str
            
            # Guardar el archivo
            workbook.save(output_path)
            
            return {
                "success": True,
                "file_path": output_path,
                "formulas_applied": len(formulas)
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def create_pivot_table(self, file_path, pivot_config, output_path, sheet_name=0):
        """
        Crea una tabla dinámica a partir de datos de Excel.
        
        Args:
            file_path (str): Ruta al archivo Excel
            pivot_config (dict): Configuración de la tabla dinámica
            output_path (str): Ruta donde guardar el resultado
            sheet_name (str/int, optional): Nombre o índice de la hoja
            
        Returns:
            dict: Resultado de la operación
        """
        try:
            # Verificar que el archivo existe
            if not Path(file_path).exists():
                return {"success": False, "error": f"Archivo no encontrado: {file_path}"}
            
            # Leer el archivo Excel
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            
            # Extraer configuración de la tabla dinámica
            index = pivot_config.get("index", [])
            columns = pivot_config.get("columns", [])
            values = pivot_config.get("values", [])
            aggfunc = pivot_config.get("aggfunc", "sum")
            
            # Validar que las columnas existen
            for col in index + columns + values:
                if col not in df.columns:
                    return {"success": False, "error": f"Columna no encontrada: {col}"}
            
            # Crear tabla dinámica
            pivot_table = pd.pivot_table(
                df,
                index=index,
                columns=columns,
                values=values,
                aggfunc=aggfunc
            )
            
            # Crear directorio si no existe
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Guardar tabla dinámica
            pivot_table.to_excel(output_path)
            
            return {
                "success": True,
                "file_path": output_path,
                "pivot_config": pivot_config
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def filter_data(self, file_path, filters, output_path=None, sheet_name=0):
        """
        Filtra datos de un archivo Excel.
        
        Args:
            file_path (str): Ruta al archivo Excel
            filters (dict): Filtros a aplicar
            output_path (str, optional): Ruta donde guardar el resultado
            sheet_name (str/int, optional): Nombre o índice de la hoja
            
        Returns:
            dict: Resultado de la operación
        """
        try:
            # Verificar que el archivo existe
            if not Path(file_path).exists():
                return {"success": False, "error": f"Archivo no encontrado: {file_path}"}
            
            # Leer el archivo Excel
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            
            # Aplicar filtros
            for column, condition in filters.items():
                if column not in df.columns:
                    continue
                
                if isinstance(condition, dict):
                    # Condiciones complejas
                    operator = condition.get("operator", "eq")
                    value = condition.get("value")
                    
                    if operator == "eq":
                        df = df[df[column] == value]
                    elif operator == "ne":
                        df = df[df[column] != value]
                    elif operator == "gt":
                        df = df[df[column] > value]
                    elif operator == "lt":
                        df = df[df[column] < value]
                    elif operator == "gte":
                        df = df[df[column] >= value]
                    elif operator == "lte":
                        df = df[df[column] <= value]
                    elif operator == "in":
                        df = df[df[column].isin(value)]
                    elif operator == "contains":
                        df = df[df[column].str.contains(value, na=False)]
                else:
                    # Condición simple de igualdad
                    df = df[df[column] == condition]
            
            # Si se especifica salida, guardar el resultado filtrado
            if output_path:
                # Crear directorio si no existe
                Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                
                # Guardar resultado
                df.to_excel(output_path, sheet_name=sheet_name, index=False)
            
            # Convertir a registros
            data = df.to_dict(orient='records')
            
            return {
                "success": True,
                "data": data,
                "rows": len(data),
                "columns": df.columns.tolist(),
                "output_path": output_path
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}