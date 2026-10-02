import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configurar salida UTF-8 en Windows
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Estilo gráfico limpio y profesional
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8

# ==============================================================================
# 1. CARGA DE DATOS OFICIALES (CSV)
# ==============================================================================
csv_file = 'gsi_datos_completos.csv'
if not os.path.exists(csv_file):
    raise FileNotFoundError(f"No se encontró {csv_file}")

df_raw = pd.read_csv(csv_file)

# Subconjuntos ordenados cronológicamente
df_libre = df_raw[df_raw['tipo_acceso'] == 'Ingreso Libre'].sort_values('convocatoria').copy().reset_index(drop=True)
df_promo = df_raw[df_raw['tipo_acceso'] == 'Promoción Interna'].sort_values('convocatoria').copy().reset_index(drop=True)

# Métricas directas
for d in [df_libre, df_promo]:
    d['plazas_desiertas'] = d['plazas_totales'] - d['superan_proceso_total']
    d['pct_aprobados_de_presentados'] = (d['superan_proceso_total'] / d['presentados_1ej_total'] * 100).round(2)
    d['pct_plazas_desiertas'] = (d['plazas_desiertas'] / d['plazas_totales'] * 100).round(2)
    d['pct_presentados_de_solicitudes'] = (d['presentados_1ej_total'] / d['solicitudes_total'] * 100).round(2)
    d['pct_aprobados_de_solicitudes'] = (d['superan_proceso_total'] / d['solicitudes_total'] * 100).round(2)

convocatorias = df_libre['convocatoria'].astype(str).tolist()
x = np.arange(len(convocatorias))

# ==============================================================================
# 2. CONSTRUCCIÓN DE TABLAS LIMPIAS Y DIRECTAS
# ==============================================================================

# TABLA 1: INGRESO LIBRE
tabla_libre = pd.DataFrame({
    'Convocatoria': df_libre['convocatoria'].astype(str),
    'Plazas Convocadas': df_libre['plazas_totales'],
    'Solicitudes (Instancias)': df_libre['solicitudes_total'],
    'Presentados (Al examen)': df_libre['presentados_1ej_total'],
    'Aprobados (Logran plaza)': df_libre['superan_proceso_total'],
    '% Aprobados / Presentados': df_libre['pct_aprobados_de_presentados'].map('{:.2f}%'.format),
    'Plazas Desiertas': df_libre['plazas_desiertas'],
    '% Plazas Desiertas': df_libre['pct_plazas_desiertas'].map('{:.2f}%'.format)
})

# Fila total histórico libre
tot_lib_plz = df_libre['plazas_totales'].sum()
tot_lib_sol = df_libre['solicitudes_total'].sum()
tot_lib_pres = df_libre['presentados_1ej_total'].sum()
tot_lib_apr = df_libre['superan_proceso_total'].sum()
tot_lib_des = df_libre['plazas_desiertas'].sum()
fila_tot_libre = pd.DataFrame([{
    'Convocatoria': 'TOTAL HISTÓRICO',
    'Plazas Convocadas': tot_lib_plz,
    'Solicitudes (Instancias)': tot_lib_sol,
    'Presentados (Al examen)': tot_lib_pres,
    'Aprobados (Logran plaza)': tot_lib_apr,
    '% Aprobados / Presentados': f'{tot_lib_apr/tot_lib_pres*100:.2f}%',
    'Plazas Desiertas': tot_lib_des,
    '% Plazas Desiertas': f'{tot_lib_des/tot_lib_plz*100:.2f}%'
}])
tabla_libre = pd.concat([tabla_libre, fila_tot_libre], ignore_index=True)

# TABLA 2: PROMOCIÓN INTERNA
tabla_promo = pd.DataFrame({
    'Convocatoria': df_promo['convocatoria'].astype(str),
    'Plazas Convocadas': df_promo['plazas_totales'],
    'Solicitudes (Instancias)': df_promo['solicitudes_total'],
    'Presentados (Al examen)': df_promo['presentados_1ej_total'],
    'Aprobados (Logran plaza)': df_promo['superan_proceso_total'],
    '% Aprobados / Presentados': df_promo['pct_aprobados_de_presentados'].map('{:.2f}%'.format),
    'Plazas Desiertas': df_promo['plazas_desiertas'],
    '% Plazas Desiertas': df_promo['pct_plazas_desiertas'].map('{:.2f}%'.format)
})
tot_pro_plz = df_promo['plazas_totales'].sum()
tot_pro_sol = df_promo['solicitudes_total'].sum()
tot_pro_pres = df_promo['presentados_1ej_total'].sum()
tot_pro_apr = df_promo['superan_proceso_total'].sum()
tot_pro_des = df_promo['plazas_desiertas'].sum()
fila_tot_promo = pd.DataFrame([{
    'Convocatoria': 'TOTAL HISTÓRICO',
    'Plazas Convocadas': tot_pro_plz,
    'Solicitudes (Instancias)': tot_pro_sol,
    'Presentados (Al examen)': tot_pro_pres,
    'Aprobados (Logran plaza)': tot_pro_apr,
    '% Aprobados / Presentados': f'{tot_pro_apr/tot_pro_pres*100:.2f}%',
    'Plazas Desiertas': tot_pro_des,
    '% Plazas Desiertas': f'{tot_pro_des/tot_pro_plz*100:.2f}%'
}])
tabla_promo = pd.concat([tabla_promo, fila_tot_promo], ignore_index=True)

# TABLA 3: TOTAL GSI CONVOCADO ESE AÑO (LIBRE + PROMO)
tot_plz_yr = df_libre['plazas_totales'] + df_promo['plazas_totales']
tot_sol_yr = df_libre['solicitudes_total'] + df_promo['solicitudes_total']
tot_pres_yr = df_libre['presentados_1ej_total'] + df_promo['presentados_1ej_total']
tot_apr_yr = df_libre['superan_proceso_total'] + df_promo['superan_proceso_total']
tot_des_yr = tot_plz_yr - tot_apr_yr

tabla_total_gsi = pd.DataFrame({
    'Convocatoria': convocatorias,
    'Plazas Convocadas': tot_plz_yr,
    'Solicitudes (Instancias)': tot_sol_yr,
    'Presentados (Al examen)': tot_pres_yr,
    'Aprobados (Logran plaza)': tot_apr_yr,
    '% Aprobados / Presentados': (tot_apr_yr / tot_pres_yr * 100).round(2).map('{:.2f}%'.format),
    'Plazas Desiertas ese Año': tot_des_yr,
    '% Plazas Desiertas': (tot_des_yr / tot_plz_yr * 100).round(2).map('{:.2f}%'.format)
})
fila_tot_global = pd.DataFrame([{
    'Convocatoria': 'TOTAL HISTÓRICO',
    'Plazas Convocadas': tot_plz_yr.sum(),
    'Solicitudes (Instancias)': tot_sol_yr.sum(),
    'Presentados (Al examen)': tot_pres_yr.sum(),
    'Aprobados (Logran plaza)': tot_apr_yr.sum(),
    '% Aprobados / Presentados': f'{tot_apr_yr.sum()/tot_pres_yr.sum()*100:.2f}%',
    'Plazas Desiertas ese Año': tot_des_yr.sum(),
    '% Plazas Desiertas': f'{tot_des_yr.sum()/tot_plz_yr.sum()*100:.2f}%'
}])
tabla_total_gsi = pd.concat([tabla_total_gsi, fila_tot_global], ignore_index=True)

# TABLA 4: CONVOCATORIA 2024 AL DETALLE POR CUPOS (DATOS DE LA IMAGEN OFICIAL)
tabla_2024_cupos = pd.DataFrame([
    {
        'Modalidad / Cupo': 'Ingreso Libre - Cupo General',
        'Plazas Convocadas': 937, 'Solicitudes': 2389, 'Presentados 1º Ej': 1004,
        'Superan Proceso (Plaza)': 397, '% Superan / Presentados': '39.54%',
        'Plazas Desiertas': 540, '% Plazas Desiertas': '57.63%'
    },
    {
        'Modalidad / Cupo': 'Ingreso Libre - Discapacidad (CRD)',
        'Plazas Convocadas': 58, 'Solicitudes': 93, 'Presentados 1º Ej': 29,
        'Superan Proceso (Plaza)': 13, '% Superan / Presentados': '44.83%',
        'Plazas Desiertas': 45, '% Plazas Desiertas': '77.59%'
    },
    {
        'Modalidad / Cupo': 'TOTAL INGRESO LIBRE 2024',
        'Plazas Convocadas': 995, 'Solicitudes': 2482, 'Presentados 1º Ej': 1033,
        'Superan Proceso (Plaza)': 410, '% Superan / Presentados': '39.69%',
        'Plazas Desiertas': 585, '% Plazas Desiertas': '58.79%'
    },
    {
        'Modalidad / Cupo': 'Promoción Interna - Cupo General',
        'Plazas Convocadas': 754, 'Solicitudes': 366, 'Presentados 1º Ej': 178,
        'Superan Proceso (Plaza)': 155, '% Superan / Presentados': '87.08%',
        'Plazas Desiertas': 599, '% Plazas Desiertas': '79.44%'
    },
    {
        'Modalidad / Cupo': 'Promoción Interna - Discapacidad (CRD)',
        'Plazas Convocadas': 46, 'Solicitudes': 19, 'Presentados 1º Ej': 8,
        'Superan Proceso (Plaza)': 7, '% Superan / Presentados': '87.50%',
        'Plazas Desiertas': 39, '% Plazas Desiertas': '84.78%'
    },
    {
        'Modalidad / Cupo': 'TOTAL PROMOCIÓN INTERNA 2024',
        'Plazas Convocadas': 800, 'Solicitudes': 385, 'Presentados 1º Ej': 186,
        'Superan Proceso (Plaza)': 162, '% Superan / Presentados': '87.10%',
        'Plazas Desiertas': 638, '% Plazas Desiertas': '79.75%'
    },
    {
        'Modalidad / Cupo': 'TOTAL CONJUNTO GSI 2024',
        'Plazas Convocadas': 1795, 'Solicitudes': 2867, 'Presentados 1º Ej': 1219,
        'Superan Proceso (Plaza)': 572, '% Superan / Presentados': '46.92%',
        'Plazas Desiertas': 1223, '% Plazas Desiertas': '68.13%'
    }
])

# ==============================================================================
# 3. GENERACIÓN DE GRÁFICOS DIRECTOS Y CLAROS
# ==============================================================================

# GRÁFICO 1: Solicitudes vs Presentados vs Aprobados (Ingreso Libre)
fig, ax = plt.subplots(figsize=(12, 6))
width_grp = 0.25
b_sol = ax.bar(x - width_grp, df_libre['solicitudes_total'], width_grp, label='Echaron la Solicitud', color='#457B9D', alpha=0.75)
b_pres = ax.bar(x, df_libre['presentados_1ej_total'], width_grp, label='Se Presentaron al Examen', color='#1D3557', alpha=0.9)
b_apr = ax.bar(x + width_grp, df_libre['superan_proceso_total'], width_grp, label='Lograron Aprobar (Plaza)', color='#2A9D8F', alpha=0.95)

ax.set_title('INGRESO LIBRE: SOLICITUDES vs PRESENTADOS vs APROBADOS', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Convocatoria', fontsize=12, fontweight='bold')
ax.set_ylabel('Número de Personas', fontsize=12, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(convocatorias, fontsize=11)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3, axis='y')
ax.set_ylim(0, max(df_libre['solicitudes_total']) * 1.15)

for bars in [b_sol, b_pres, b_apr]:
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., h + 30, f'{int(h)}', ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('01_solicitudes_presentados_aprobados.png', dpi=150, bbox_inches='tight')
plt.close()

# GRÁFICO 2: De los que se presentaron, ¿cuántos lograron aprobar? (%)
fig, ax = plt.subplots(figsize=(11, 5.5))
ax.plot(convocatorias, df_libre['pct_aprobados_de_presentados'], 'o-', linewidth=3.5, markersize=10, 
        label='Ingreso Libre (% Aprobados / Presentados)', color='#1D3557', markeredgecolor='white', markeredgewidth=2)
ax.plot(convocatorias, df_promo['pct_aprobados_de_presentados'], 's-', linewidth=3.5, markersize=10, 
        label='Promoción Interna (% Aprobados / Presentados)', color='#E63946', markeredgecolor='white', markeredgewidth=2)

ax.set_xlabel('Convocatoria', fontsize=12, fontweight='bold', labelpad=10)
ax.set_ylabel('% de Aprobados sobre Presentados', fontsize=12, fontweight='bold')
ax.set_title('DE LOS QUE SE PRESENTARON AL EXAMEN, ¿QUÉ % LOGRÓ APROBAR?', fontsize=14, fontweight='bold', pad=15)
ax.set_ylim(0, 105)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=11, loc='upper left')

for i, (v_lib, v_pro) in enumerate(zip(df_libre['pct_aprobados_de_presentados'], df_promo['pct_aprobados_de_presentados'])):
    ax.annotate(f'{v_lib:.1f}%', (i, v_lib), textcoords="offset points", xytext=(0, 10),
                ha='center', fontsize=10, fontweight='bold', color='#1D3557')
    ax.annotate(f'{v_pro:.1f}%', (i, v_pro), textcoords="offset points", xytext=(0, 10),
                ha='center', fontsize=10, fontweight='bold', color='#E63946')

plt.tight_layout()
plt.savefig('02_porcentaje_aprobados_de_presentados.png', dpi=150, bbox_inches='tight')
plt.close()

# GRÁFICO 3: Plazas Convocadas vs Desiertas (Total GSI Convocado ese año)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5.5))

# Libre
b1 = ax1.bar(convocatorias, df_libre['superan_proceso_total'], width=0.55, label='Plazas Cubiertas', color='#2A9D8F', alpha=0.9)
b2 = ax1.bar(convocatorias, df_libre['plazas_desiertas'], width=0.55, bottom=df_libre['superan_proceso_total'], label='Plazas Desiertas', color='#E76F51', alpha=0.85)
ax1.set_title('Ingreso Libre: Plazas Convocadas vs Desiertas', fontsize=12, fontweight='bold', pad=12)
ax1.set_xlabel('Convocatoria', fontsize=11, fontweight='bold')
ax1.set_ylabel('Plazas', fontsize=11, fontweight='bold')
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3, axis='y')
ax1.set_ylim(0, 1250)

for i in range(len(convocatorias)):
    tot = df_libre['plazas_totales'].iloc[i]
    des = df_libre['plazas_desiertas'].iloc[i]
    cub = df_libre['superan_proceso_total'].iloc[i]
    pct_d = df_libre['pct_plazas_desiertas'].iloc[i]
    ax1.text(i, tot + 25, f'Total: {tot}\n{des} desiertas ({pct_d:.1f}%)', ha='center', va='bottom', fontsize=9, fontweight='bold', color='#E63946')
    ax1.text(i, cub/2, f'{cub}', ha='center', va='center', color='white', fontweight='bold', fontsize=10)
    ax1.text(i, cub + des/2, f'{des}', ha='center', va='center', color='white', fontweight='bold', fontsize=10)

# Total GSI (Libre + Promo)
b_g1 = ax2.bar(convocatorias, tot_apr_yr, width=0.55, label='Plazas Cubiertas (Total GSI)', color='#2A9D8F', alpha=0.9)
b_g2 = ax2.bar(convocatorias, tot_des_yr, width=0.55, bottom=tot_apr_yr, label='Plazas Desiertas (Total GSI)', color='#E76F51', alpha=0.85)
ax2.set_title('TOTAL GSI (Libre + Promo): Plazas Convocadas vs Desiertas', fontsize=12, fontweight='bold', pad=12)
ax2.set_xlabel('Convocatoria', fontsize=11, fontweight='bold')
ax2.set_ylabel('Plazas', fontsize=11, fontweight='bold')
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3, axis='y')
ax2.set_ylim(0, 2250)

for i in range(len(convocatorias)):
    tot_g = tot_plz_yr.iloc[i]
    des_g = tot_des_yr.iloc[i]
    cub_g = tot_apr_yr.iloc[i]
    pct_dg = des_g / tot_g * 100
    ax2.text(i, tot_g + 35, f'Total: {tot_g}\n{des_g} desiertas ({pct_dg:.1f}%)', 
             ha='center', va='bottom', fontsize=9, fontweight='bold', color='#E63946')
    ax2.text(i, cub_g/2, f'{cub_g}', ha='center', va='center', color='white', fontweight='bold', fontsize=10)
    ax2.text(i, cub_g + des_g/2, f'{des_g}', ha='center', va='center', color='white', fontweight='bold', fontsize=10)

plt.suptitle('¿CUÁNTAS PLAZAS QUEDAN DESIERTAS DE TODAS LAS CONVOCADAS ESE AÑO?', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('03_plazas_convocadas_vs_desiertas.png', dpi=150, bbox_inches='tight')
plt.close()

# ==============================================================================
# 4. SALIDA EN CONSOLA (TABLAS FORMATEADAS)
# ==============================================================================
print("\n" + "="*95)
print("1. INGRESO LIBRE: SOLICITUDES, PRESENTADOS, APROBADOS Y PLAZAS DESIERTAS")
print("="*95)
print(tabla_libre.to_string(index=False))

print("\n" + "="*95)
print("2. PROMOCIÓN INTERNA: SOLICITUDES, PRESENTADOS, APROBADOS Y PLAZAS DESIERTAS")
print("="*95)
print(tabla_promo.to_string(index=False))

print("\n" + "="*95)
print("3. RADIOGRAFÍA EXACTA CONVOCATORIA 2024 (DATOS OFICIALES DE LA MEMORIA)")
print("="*95)
print(tabla_2024_cupos.to_string(index=False))

print("\n" + "="*95)
print("4. RESUMEN: ¿CUÁNTAS PLAZAS QUEDAN DESIERTAS DE TODAS LAS CONVOCADAS ESE AÑO? (TOTAL GSI)")
print("="*95)
print(tabla_total_gsi.to_string(index=False))

print("\n" + "="*95)
print("✅ Gráficos generados:")
print("   - 01_solicitudes_presentados_aprobados.png")
print("   - 02_porcentaje_aprobados_de_presentados.png")
print("   - 03_plazas_convocadas_vs_desiertas.png")
print("="*95)
