from MailTagCount import contar_correos_etiquetas,filtrar_etiquetas,contar_correos_etiquetas_total

if __name__ == "__main__":
    print('Proccess Started..')
    dataframe_etiquetas = contar_correos_etiquetas()
    dataframe_etiquetas_filtrado = filtrar_etiquetas(dataframe_etiquetas)
    dataframe_etiquetas_filtrado.to_excel('etiquetas_correos_filtrado.xlsx', index=False)
    print("Archivo Excel exportado exitosamente.")
    dataframe_etiquetas_total = contar_correos_etiquetas_total()
    dataframe_etiquetas_total_filtrado=filtrar_etiquetas(dataframe_etiquetas_total)
    dataframe_etiquetas_total_filtrado.to_excel('etiquetas_correos_totalizados.xlsx', index=False)
    print("Archivo Excel Totales exportado exitosamente.")