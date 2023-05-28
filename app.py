import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import shutil

plt.style.use('ggplot')

# Leer el archivo CSV
df = pd.read_csv('data.csv')

# Convertir la columna 'Created Time' a datetime
df['Created Time'] = pd.to_datetime(df['Created Time'])

# Filtrar ordenes de compra y venta
sell_orders = df[df['Order Type'] == 'Sell']
buy_orders = df[df['Order Type'] == 'Buy']

# Generar estadisticas basicas
total_orders = df.shape[0]
total_sell_orders = sell_orders.shape[0]
total_buy_orders = buy_orders.shape[0]
total_USDT_sold = sell_orders[sell_orders['Asset Type'] == 'USDT']['Quantity'].sum()
total_USDT_bought = buy_orders[buy_orders['Asset Type'] == 'USDT']['Quantity'].sum()

# Precio promedio de venta y compra
avg_sell_price = sell_orders['Price'].mean()
avg_buy_price = buy_orders['Price'].mean()

# Porcentaje promedio de ganancia
avg_gain = (avg_sell_price - avg_buy_price) / avg_buy_price * 100

# Tarifa de Binance
fee_rate = 0.0028

# Ganancia total despues de tarifas
sell_gain = (avg_sell_price - 1 - fee_rate) * total_USDT_sold
buy_loss = (1 - avg_buy_price - fee_rate) * total_USDT_bought
total_gain = sell_gain + buy_loss

# Volumen promedio de venta y compra
avg_sell_volume = sell_orders['Quantity'].mean()
avg_buy_volume = buy_orders['Quantity'].mean()

# Alinear los indices
index = pd.date_range(min(df['Created Time'].dt.date), max(df['Created Time'].dt.date))

# Crear carpeta si no existe
os.makedirs('Estadisticas', exist_ok=True)

# Volumen promedio diario
daily_volume_sell = sell_orders.groupby(sell_orders['Created Time'].dt.date)['Quantity'].sum()
daily_volume_sell = daily_volume_sell.reindex(index, fill_value=0)
daily_volume_buy = buy_orders.groupby(buy_orders['Created Time'].dt.date)['Quantity'].sum()
daily_volume_buy = daily_volume_buy.reindex(index, fill_value=0)

# Grafico de volumen diario
plt.bar(daily_volume_sell.index, daily_volume_sell, color='red', label='Venta')
plt.title('Volumen Diario de Venta')
plt.xlabel('Fecha')
plt.ylabel('Volumen')
plt.legend()
plt.xticks(rotation=45)
plt.savefig('Estadisticas/volumen_diario_venta.png')
plt.close()

plt.bar(daily_volume_buy.index, daily_volume_buy, color='green', label='Compra')
plt.title('Volumen Diario de Compra')
plt.xlabel('Fecha')
plt.ylabel('Volumen')
plt.legend()
plt.xticks(rotation=45)
plt.savefig('Estadisticas/volumen_diario_compra.png')
plt.close()

# Cantidad de ordenes diarias
daily_orders_sell = sell_orders.groupby(sell_orders['Created Time'].dt.date)['Order Type'].count()
daily_orders_sell = daily_orders_sell.reindex(index, fill_value=0)
daily_orders_buy = buy_orders.groupby(buy_orders['Created Time'].dt.date)['Order Type'].count()
daily_orders_buy = daily_orders_buy.reindex(index, fill_value=0)

# Grafico de ordenes diarias
plt.bar(daily_orders_sell.index, daily_orders_sell, color='red', label='Venta')
plt.title('Ordenes Diarias de Venta')
plt.xlabel('Fecha')
plt.ylabel('Cantidad de ordenes')
plt.legend()
plt.xticks(rotation=45)
plt.savefig('Estadisticas/ordenes_diarias_venta.png')
plt.close()

plt.bar(daily_orders_buy.index, daily_orders_buy, color='green', label='Compra')
plt.title('Ordenes Diarias de Compra')
plt.xlabel('Fecha')
plt.ylabel('Cantidad de ordenes')
plt.legend()
plt.xticks(rotation=45)
plt.savefig('Estadisticas/ordenes_diarias_compra.png')
plt.close()

# Resto del código para análisis de datos y generación de estadísticas

# Volumen promedio semanal
weekly_volume = df.groupby(pd.Grouper(key='Created Time', freq='W'))['Quantity'].sum()
weekly_volume = weekly_volume.reindex(index, fill_value=0)

# Grafico de volumen semanal
plt.bar(weekly_volume.index, weekly_volume, color='blue', label='Volumen Semanal')
plt.title('Volumen Semanal')
plt.xlabel('Semana')
plt.ylabel('Volumen')
plt.legend()
plt.xticks(rotation=45)
plt.savefig('Estadisticas/volumen_semanal.png')
plt.close()

# Ganancia promedio por orden
avg_gain_per_order = total_gain / total_orders

# Ganancia promedio diaria
avg_daily_gain = total_gain / df['Created Time'].dt.date.nunique()

# Análisis horario
df['Hour'] = df['Created Time'].dt.hour
hourly_volume = df.groupby('Hour')['Quantity'].sum()
hourly_orders = df.groupby('Hour')['Order Type'].count()

plt.figure(figsize=(10, 5))
sns.lineplot(data=hourly_volume)
plt.title('Volumen por hora del día')
plt.xlabel('Hora del día')
plt.ylabel('Volumen')
plt.xticks(range(24))
plt.savefig('Estadisticas/volumen_por_hora.png')
plt.close()

plt.figure(figsize=(10, 5))
sns.lineplot(data=hourly_orders)
plt.title('Ordenes por hora del día')
plt.xlabel('Hora del día')
plt.ylabel('Cantidad de ordenes')
plt.xticks(range(24))
plt.savefig('Estadisticas/ordenes_por_hora.png')
plt.close()

# Grafico de dispersión: Precio vs Volumen de ordenes de venta
plt.scatter(sell_orders['Price'], sell_orders['Quantity'])
plt.title('Relación entre Precio y Volumen de Ordenes de Venta')
plt.xlabel('Precio')
plt.ylabel('Volumen')
plt.savefig('Estadisticas/precio_vs_volumen.png')
plt.close()

# Generar el archivo Markdown
with open('Estadisticas/estadisticas.md', 'w') as file:
    file.write('# Estadisticas\n\n')
    file.write(f'- Total de ordenes: {total_orders}\n')
    file.write(f'- Total de ordenes de venta: {total_sell_orders}\n')
    file.write(f'- Total de ordenes de compra: {total_buy_orders}\n')
    file.write(f'- Total de USDT vendidos: {total_USDT_sold:.2f}\n')
    file.write(f'- Total de USDT comprados: {total_USDT_bought:.2f}\n')
    file.write(f'- Precio promedio de venta: {avg_sell_price:.2f}\n')
    file.write(f'- Precio promedio de compra: {avg_buy_price:.2f}\n')
    file.write(f'- Porcentaje promedio de ganancia: {avg_gain:.2f}%\n')
    file.write(f'- Ganancia total despues de tarifas: {total_gain:.2f}\n')
    file.write(f'- Volumen promedio de venta: {avg_sell_volume:.2f}\n')
    file.write(f'- Volumen promedio de compra: {avg_buy_volume:.2f}\n')
    file.write(f'- Ganancia promedio por orden: {avg_gain_per_order:.2f}\n')
    file.write(f'- Ganancia promedio diaria: {avg_daily_gain:.2f}\n\n')

    # Mover archivos generados a la carpeta "Estadisticas"
    shutil.move('Estadisticas/volumen_diario_venta.png', 'Estadisticas/volumen_diario_venta.png')
    shutil.move('Estadisticas/volumen_diario_compra.png', 'Estadisticas/volumen_diario_compra.png')
    shutil.move('Estadisticas/ordenes_diarias_venta.png', 'Estadisticas/ordenes_diarias_venta.png')
    shutil.move('Estadisticas/ordenes_diarias_compra.png', 'Estadisticas/ordenes_diarias_compra.png')
    shutil.move('Estadisticas/volumen_semanal.png', 'Estadisticas/volumen_semanal.png')
    shutil.move('Estadisticas/volumen_por_hora.png', 'Estadisticas/volumen_por_hora.png')
    shutil.move('Estadisticas/ordenes_por_hora.png', 'Estadisticas/ordenes_por_hora.png')
    shutil.move('Estadisticas/precio_vs_volumen.png', 'Estadisticas/precio_vs_volumen.png')

    # Graficos
    file.write('## Graficos\n\n')
    file.write('### Volumen Diario de Venta\n\n')
    file.write('![Volumen Diario de Venta](volumen_diario_venta.png)\n\n')
    file.write('### Volumen Diario de Compra\n\n')
    file.write('![Volumen Diario de Compra](volumen_diario_compra.png)\n\n')
    file.write('### Ordenes Diarias de Venta\n\n')
    file.write('![Ordenes Diarias de Venta](ordenes_diarias_venta.png)\n\n')
    file.write('### Ordenes Diarias de Compra\n\n')
    file.write('![Ordenes Diarias de Compra](ordenes_diarias_compra.png)\n\n')
    file.write('### Volumen Semanal\n\n')
    file.write('![Volumen Semanal](volumen_semanal.png)\n\n')
    file.write('### Volumen por hora del día\n\n')
    file.write('![Volumen por hora del día](volumen_por_hora.png)\n\n')
    file.write('### Ordenes por hora del día\n\n')
    file.write('![Ordenes por hora del día](ordenes_por_hora.png)\n\n')
    file.write('### Relación entre Precio y Volumen de Ordenes de Venta\n\n')
    file.write('![Relación entre Precio y Volumen de Ordenes de Venta](precio_vs_volumen.png)\n\n')
