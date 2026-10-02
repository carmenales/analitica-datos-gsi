import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# ============================================
# CONFIGURACIÓN DE ESTILO
# ============================================
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8

# ============================================
# 1. CARGA DE DATOS OFICIALES (CSV)
# ============================================
csv_file = 'gsi_datos_completos.csv'
if not os.path.exists(csv_file):
    raise FileNotFoundError(f"No se encontró el archivo {csv_file}. Asegúrate de ejecutar en el directorio raíz.")

df_raw = pd.read_csv(csv_file)

# Separar y ordenar cronológicamente
df_libre = df_raw[df_raw['tipo_acceso'] == 'Ingreso Libre'].sort_values('convocatoria').copy().reset_index(drop=True)
df_promo = df_raw[df_raw['tipo_acceso'] == 'Promoción Interna'].sort_values('convocatoria').copy().reset_index(drop=True)

# Calcular métricas dinámicas
for d in [df_libre, df_promo]:
    d['tasa_presentacion'] = (d['presentados_1ej_total'] / d['solicitudes_total'] * 100).round(2)
    d['tasa_abandono'] = (100 - d['tasa_presentacion']).round(2)
    d['tasa_exito_global'] = (d['superan_proceso_total'] / d['presentados_1ej_total'] * 100).round(2)
    d['tasa_cobertura'] = (d['superan_proceso_total'] / d['plazas_totales'] * 100).round(2)
    d['plazas_desiertas'] = d['plazas_totales'] - d['superan_proceso_total']
    d['pct_desiertas'] = (d['plazas_desiertas'] / d['plazas_totales'] * 100).round(2)
    d['ratio_solicitudes_plaza'] = (d['solicitudes_total'] / d['plazas_totales']).round(2)
    d['ratio_presentados_plaza'] = (d['presentados_1ej_total'] / d['plazas_totales']).round(2)

convocatorias = df_libre['convocatoria'].astype(str).tolist()
x = np.arange(len(convocatorias))
width = 0.35

print("✅ Datos oficiales cargados correctamente desde CSV")
print(f"Convocatorias analizadas: {convocatorias}")

# ============================================
# 2. GRÁFICO 1: EVOLUCIÓN TASA DE ÉXITO
# ============================================
fig, ax = plt.subplots(figsize=(11, 5.5))

ax.plot(convocatorias, df_libre['tasa_exito_global'], 'o-', linewidth=3, markersize=9, 
        label='Ingreso Libre', color='#1D3557', markeredgecolor='white', markeredgewidth=2)
ax.plot(convocatorias, df_promo['tasa_exito_global'], 's-', linewidth=3, markersize=9, 
        label='Promoción Interna', color='#E63946', markeredgecolor='white', markeredgewidth=2)

ax.set_xlabel('Convocatoria (Año de examen)', fontsize=12, fontweight='bold', labelpad=10)
ax.set_ylabel('Tasa de Éxito Global (%)', fontsize=12, fontweight='bold')
ax.set_title('EVOLUCIÓN TASA DE ÉXITO (2018-2024)\n% de aspirantes presentados que obtienen plaza', 
             fontsize=14, fontweight='bold', pad=15)
ax.legend(fontsize=11, loc='upper left')
ax.set_ylim(0, 105)
ax.grid(True, alpha=0.3)

for i, (v_lib, v_pro) in enumerate(zip(df_libre['tasa_exito_global'], df_promo['tasa_exito_global'])):
    ax.annotate(f'{v_lib:.1f}%', (i, v_lib), textcoords="offset points", xytext=(0, 10),
                ha='center', fontsize=10, fontweight='bold', color='#1D3557')
    ax.annotate(f'{v_pro:.1f}%', (i, v_pro), textcoords="offset points", xytext=(0, 10),
                ha='center', fontsize=10, fontweight='bold', color='#E63946')

plt.tight_layout()
plt.savefig('01_tasa_exito.png', dpi=150, bbox_inches='tight')
plt.close()

# ============================================
# 3. GRÁFICO 2: COMPETITIVIDAD (REAL vs TEÓRICA)
# ============================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), sharey=True)

bars_sol_lib = ax1.bar(x - width/2, df_libre['ratio_solicitudes_plaza'], width,
                       label='Solicitudes/Plaza (Teórico)', color='#457B9D', alpha=0.7)
bars_pres_lib = ax1.bar(x + width/2, df_libre['ratio_presentados_plaza'], width,
                        label='Presentados/Plaza (Real)', color='#1D3557', alpha=0.95)

ax1.set_title('INGRESO LIBRE: Competencia Real vs Aparente', fontsize=13, fontweight='bold', pad=12)
ax1.set_xlabel('Convocatoria', fontsize=11, fontweight='bold')
ax1.set_ylabel('Opositores por Plaza', fontsize=11, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(convocatorias, fontsize=10)
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3, axis='y')

for bar in bars_sol_lib:
    h = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., h + 0.15, f'{h:.2f}', ha='center', va='bottom', fontsize=9)
for bar in bars_pres_lib:
    h = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., h + 0.15, f'{h:.2f}', ha='center', va='bottom', fontsize=9, fontweight='bold', color='#1D3557')

bars_sol_pro = ax2.bar(x - width/2, df_promo['ratio_solicitudes_plaza'], width,
                       label='Solicitudes/Plaza (Teórico)', color='#F4A261', alpha=0.7)
bars_pres_pro = ax2.bar(x + width/2, df_promo['ratio_presentados_plaza'], width,
                        label='Presentados/Plaza (Real)', color='#E76F51', alpha=0.95)

ax2.set_title('PROMOCIÓN INTERNA: Ratios de Competencia', fontsize=13, fontweight='bold', pad=12)
ax2.set_xlabel('Convocatoria', fontsize=11, fontweight='bold')
ax2.set_xticks(x)
ax2.set_xticklabels(convocatorias, fontsize=10)
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3, axis='y')
ax2.axhline(1.0, color='gray', linestyle='--', linewidth=1, alpha=0.7, label='Ratio 1:1')

for bar in bars_sol_pro:
    h = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., h + 0.15, f'{h:.2f}', ha='center', va='bottom', fontsize=9)
for bar in bars_pres_pro:
    h = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., h + 0.15, f'{h:.2f}', ha='center', va='bottom', fontsize=9, fontweight='bold', color='#E76F51')

plt.suptitle('RATIO DE COMPETITIVIDAD: SOLICITANTES vs PRESENTADOS REALES', fontsize=15, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('02_competitividad.png', dpi=150, bbox_inches='tight')
plt.close()

# ============================================
# 4. GRÁFICO 3: PLAZAS CONVOCADAS (CUBIERTAS vs DESIERTAS)
# ============================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

def plot_stacked_cobertura(ax, df_sub, titulo, color_cubiertas='#2A9D8F', color_desiertas='#E76F51'):
    cubiertas = df_sub['superan_proceso_total'].values
    desiertas = df_sub['plazas_desiertas'].values
    plazas = df_sub['plazas_totales'].values
    cobertura = df_sub['tasa_cobertura'].values
    
    b1 = ax.bar(x, cubiertas, width=0.55, label='Plazas Cubiertas (Aprobados)', color=color_cubiertas, alpha=0.9, edgecolor='white')
    b2 = ax.bar(x, desiertas, width=0.55, bottom=cubiertas, label='Plazas Desiertas (Sin cubrir)', color=color_desiertas, alpha=0.75, edgecolor='white')
    
    ax.set_title(titulo, fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel('Convocatoria', fontsize=11, fontweight='bold')
    ax.set_ylabel('Número de Plazas', fontsize=11, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(convocatorias, fontsize=10)
    ax.legend(fontsize=10, loc='upper left')
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_ylim(0, max(plazas) * 1.25)
    
    for i in range(len(df_sub)):
        if cubiertas[i] > 40:
            ax.text(i, cubiertas[i]/2, f'{cubiertas[i]}', ha='center', va='center', color='white', fontweight='bold', fontsize=10)
        if desiertas[i] > 40:
            ax.text(i, cubiertas[i] + desiertas[i]/2, f'{desiertas[i]}', ha='center', va='center', color='white', fontweight='bold', fontsize=10)
        ax.text(i, plazas[i] + (max(plazas)*0.03), f'Total: {plazas[i]}\n({cobertura[i]:.1f}% cubiertas\n{100-cobertura[i]:.1f}% desiertas)',
                ha='center', va='bottom', fontsize=9, fontweight='bold', color='#264653')

plot_stacked_cobertura(ax1, df_libre, 'INGRESO LIBRE: PLAZAS CUBIERTAS vs DESIERTAS')
plot_stacked_cobertura(ax2, df_promo, 'PROMOCIÓN INTERNA: PLAZAS CUBIERTAS vs DESIERTAS', '#457B9D', '#E63946')

plt.suptitle('BALANCE DE PLAZAS: ALTA PROPORCIÓN DE PLAZAS DESIERTAS', fontsize=15, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('03_plazas_vs_aprobados.png', dpi=150, bbox_inches='tight')
plt.close()

# ============================================
# 5. GRÁFICO 4: EMBUDO DE CONVERSIÓN (INGRESO LIBRE)
# ============================================
fig, ax = plt.subplots(figsize=(12, 6))

etapas = ['Solicitudes', 'Admitidos', 'Presentados\n(Examen)', 'Aprobados\n(Plaza)']

vals_2024 = [
    df_libre.loc[df_libre['convocatoria'] == 2024, 'solicitudes_total'].values[0],
    df_libre.loc[df_libre['convocatoria'] == 2024, 'admitidos_total'].values[0],
    df_libre.loc[df_libre['convocatoria'] == 2024, 'presentados_1ej_total'].values[0],
    df_libre.loc[df_libre['convocatoria'] == 2024, 'superan_proceso_total'].values[0]
]

vals_2019 = [
    df_libre.loc[df_libre['convocatoria'] == 2019, 'solicitudes_total'].values[0],
    df_libre.loc[df_libre['convocatoria'] == 2019, 'admitidos_total'].values[0],
    df_libre.loc[df_libre['convocatoria'] == 2019, 'presentados_1ej_total'].values[0],
    df_libre.loc[df_libre['convocatoria'] == 2019, 'superan_proceso_total'].values[0]
]

x_funnel = np.arange(len(etapas))
w_funnel = 0.35

b_2024 = ax.bar(x_funnel - w_funnel/2, vals_2024, w_funnel, label='Ingreso Libre 2024', color='#1D3557', alpha=0.9)
b_2019 = ax.bar(x_funnel + w_funnel/2, vals_2019, w_funnel, label='Ingreso Libre 2019', color='#457B9D', alpha=0.7)

ax.set_title('EMBUDO DE CONVERSIÓN EN INGRESO LIBRE: ¿DÓNDE SE PIERDEN LOS CANDIDATOS?', fontsize=14, fontweight='bold', pad=15)
ax.set_ylabel('Número de Aspirantes', fontsize=12, fontweight='bold')
ax.set_xticks(x_funnel)
ax.set_xticklabels(etapas, fontsize=11, fontweight='bold')
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3, axis='y')

for bar, base in [(b_2024, vals_2024[0]), (b_2019, vals_2019[0])]:
    for rect in bar:
        h = rect.get_height()
        pct = (h / base) * 100
        ax.text(rect.get_x() + rect.get_width()/2., h + 35, f'{int(h)}\n({pct:.1f}%)',
                ha='center', va='bottom', fontsize=9, fontweight='bold')

ax.set_ylim(0, max(vals_2024) * 1.25)
plt.tight_layout()
plt.savefig('04_embudo_conversion.png', dpi=150, bbox_inches='tight')
plt.close()

# ============================================
# 6. GRÁFICO 5: TASA DE PRESENTACIÓN Y ABSENTISMO
# ============================================
fig, ax = plt.subplots(figsize=(11, 5.5))

b_pres = ax.bar(x - width/2, df_libre['tasa_presentacion'], width, label='Presentados al Examen (%)', color='#2A9D8F', alpha=0.9)
b_aban = ax.bar(x + width/2, df_libre['tasa_abandono'], width, label='Absentismo / Abandono Previo (%)', color='#E76F51', alpha=0.85)

ax.set_xlabel('Convocatoria', fontsize=12, fontweight='bold', labelpad=10)
ax.set_ylabel('Porcentaje (%)', fontsize=12, fontweight='bold')
ax.set_title('INGRESO LIBRE: TASA DE PRESENTACIÓN vs ABSENTISMO PRE-EXAMEN\nMás del 50% de los inscritos no acude a la prueba', 
             fontsize=14, fontweight='bold', pad=15)
ax.set_xticks(x)
ax.set_xticklabels(convocatorias, fontsize=11)
ax.legend(fontsize=11, loc='upper right')
ax.set_ylim(0, 110)
ax.grid(True, alpha=0.3, axis='y')

for bar in b_pres:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., h + 2, f'{h:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold', color='#2A9D8F')
for bar in b_aban:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., h + 2, f'{h:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold', color='#E76F51')

plt.tight_layout()
plt.savefig('05_tasa_presentacion.png', dpi=150, bbox_inches='tight')
plt.close()

# ============================================
# 7. GRÁFICO 6: INGRESO LIBRE - GENERAL vs DISCAPACIDAD
# ============================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

cobertura_gen = (df_libre['superan_proceso_general'] / df_libre['plazas_general'] * 100).round(1)
cobertura_disc = (df_libre['superan_proceso_discapacidad'] / df_libre['plazas_discapacidad'] * 100).round(1)

b_c_gen = ax1.bar(x - width/2, cobertura_gen, width, label='Cupo General', color='#1D3557', alpha=0.85)
b_c_disc = ax1.bar(x + width/2, cobertura_disc, width, label='Cupo Discapacidad', color='#E63946', alpha=0.85)

ax1.set_title('Tasa de Cobertura (% Plazas Cubiertas)', fontsize=13, fontweight='bold', pad=12)
ax1.set_xlabel('Convocatoria', fontsize=11, fontweight='bold')
ax1.set_ylabel('% de Plazas Cubiertas', fontsize=11, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(convocatorias, fontsize=10)
ax1.set_ylim(0, 100)
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3, axis='y')

for b in b_c_gen:
    ax1.text(b.get_x() + b.get_width()/2., b.get_height() + 2, f'{b.get_height():.1f}%', ha='center', fontsize=9, fontweight='bold')
for b in b_c_disc:
    ax1.text(b.get_x() + b.get_width()/2., b.get_height() + 2, f'{b.get_height():.1f}%', ha='center', fontsize=9, fontweight='bold')

ratio_p_gen = (df_libre['presentados_1ej_general'] / df_libre['plazas_general']).round(2)
ratio_p_disc = (df_libre['presentados_1ej_discapacidad'] / df_libre['plazas_discapacidad']).round(2)

b_r_gen = ax2.bar(x - width/2, ratio_p_gen, width, label='Cupo General', color='#1D3557', alpha=0.85)
b_r_disc = ax2.bar(x + width/2, ratio_p_disc, width, label='Cupo Discapacidad', color='#E63946', alpha=0.85)

ax2.set_title('Competencia Real (Presentados / Plaza)', fontsize=13, fontweight='bold', pad=12)
ax2.set_xlabel('Convocatoria', fontsize=11, fontweight='bold')
ax2.set_ylabel('Presentados por Plaza', fontsize=11, fontweight='bold')
ax2.set_xticks(x)
ax2.set_xticklabels(convocatorias, fontsize=10)
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3, axis='y')
ax2.axhline(1.0, color='gray', linestyle='--', linewidth=1, alpha=0.7, label='Ratio 1:1')

for b in b_r_gen:
    ax2.text(b.get_x() + b.get_width()/2., b.get_height() + 0.1, f'{b.get_height():.2f}', ha='center', fontsize=9)
for b in b_r_disc:
    ax2.text(b.get_x() + b.get_width()/2., b.get_height() + 0.1, f'{b.get_height():.2f}', ha='center', fontsize=9, fontweight='bold', color='#E63946')

plt.suptitle('INGRESO LIBRE: COMPARATIVA CUPO GENERAL vs CUPO DISCAPACIDAD', fontsize=15, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('06_ingreso_libre_general_vs_discapacidad.png', dpi=150, bbox_inches='tight')
plt.close()

# ============================================
# 8. GRÁFICO 7: DESGLOSE OEPs ACUMULADAS
# ============================================
csv_oep = 'gsi_oep_desglose_acumuladas.csv'
if os.path.exists(csv_oep):
    df_oep_raw = pd.read_csv(csv_oep)
    df_oep_libre = df_oep_raw[df_oep_raw['tipo_acceso'] == 'Ingreso Libre'].copy()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))
    
    # 2022
    df_2022 = df_oep_libre[df_oep_libre['convocatoria'] == 2022]
    oeps_2022 = df_2022['oep_origen'].astype(str).tolist()
    cub_2022 = df_2022['plazas_cubiertas'].values
    vac_2022 = df_2022['plazas_vacantes'].values
    
    ax1.bar(oeps_2022, cub_2022, label='Cubiertas', color='#2A9D8F', alpha=0.9)
    ax1.bar(oeps_2022, vac_2022, bottom=cub_2022, label='Vacantes / Desiertas', color='#E76F51', alpha=0.75)
    ax1.set_title('Convocatoria 2022 (840 plazas)\nOEPs 2020-2021-2022', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Año OEP de Origen', fontsize=10, fontweight='bold')
    ax1.set_ylabel('Plazas', fontsize=10, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3, axis='y')
    for i in range(len(oeps_2022)):
        ax1.text(i, cub_2022[i]/2 if cub_2022[i]>20 else 10, f'{cub_2022[i]}', ha='center', va='center', color='white', fontweight='bold')
        if vac_2022[i] > 20:
            ax1.text(i, cub_2022[i] + vac_2022[i]/2, f'{vac_2022[i]}', ha='center', va='center', color='white', fontweight='bold')

    # 2024
    df_2024 = df_oep_libre[df_oep_libre['convocatoria'] == 2024]
    oeps_2024 = df_2024['oep_origen'].astype(str).tolist()
    cub_2024 = df_2024['plazas_cubiertas'].values
    vac_2024 = df_2024['plazas_vacantes'].values
    
    ax2.bar(oeps_2024, cub_2024, label='Cubiertas', color='#2A9D8F', alpha=0.9)
    ax2.bar(oeps_2024, vac_2024, bottom=cub_2024, label='Vacantes / Desiertas', color='#E76F51', alpha=0.75)
    ax2.set_title('Convocatoria 2024 (995 plazas)\nOEPs 2021-2022-2023-2024', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Año OEP de Origen', fontsize=10, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='y')
    for i in range(len(oeps_2024)):
        if cub_2024[i] > 20:
            ax2.text(i, cub_2024[i]/2, f'{cub_2024[i]}', ha='center', va='center', color='white', fontweight='bold')
        if vac_2024[i] > 20:
            ax2.text(i, cub_2024[i] + vac_2024[i]/2, f'{vac_2024[i]}', ha='center', va='center', color='white', fontweight='bold')

    plt.suptitle('INGRESO LIBRE: ASIGNACIÓN DE APROBADOS POR AÑO DE OEP ACUMULADA', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('07_ingreso_libre_oeps_acumuladas.png', dpi=150, bbox_inches='tight')
    plt.close()

# ============================================
# 9. GRÁFICO 8: PROGRESIÓN Y CRIBA POR EJERCICIO (2018, 2019 y 2024)
# ============================================
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5.5))

def plot_progression_ejercicios(ax, conv_year):
    r = df_libre[df_libre['convocatoria'] == conv_year].iloc[0]
    p1 = r['presentados_1ej_total']
    s1 = r['superan_1ej_total']
    c1 = p1 - s1
    p2 = r['presentados_2ej_total']
    aban_2 = s1 - p2
    s2 = r['superan_2ej_total']
    c2 = p2 - s2
    
    stages = ['1º Ej (Test)\nPresentados', 'Superan 1º\nAprobados', '2º Ej (Práct.)\nPresentados', 'Superan 2º\nPlaza Final']
    vals = [p1, s1, p2, s2]
    colors = ['#1D3557', '#457B9D', '#2A9D8F', '#E76F51']
    bars = ax.bar(stages, vals, color=colors, width=0.55, edgecolor='white', linewidth=1.5)
    
    ax.set_title(f'Convocatoria {conv_year} (OEP {r["oep"]})\nPlazas: {r["plazas_totales"]} | Solicitudes: {r["solicitudes_total"]}', 
                 fontsize=11, fontweight='bold', pad=12)
    ax.set_ylabel('Número de Opositores', fontsize=10, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_ylim(0, p1 * 1.25)
    
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., h + (p1*0.02), f'{int(h)}', 
                ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    ax.annotate(f'Cae: {c1/p1*100:.1f}%\n({int(c1)} susp.)', 
                xy=(0.5, (p1 + s1)/2), xytext=(0.5, p1*0.82),
                ha='center', fontsize=8, fontweight='bold', color='#E63946',
                bbox=dict(boxstyle="round,pad=0.2", fc="#FFF0F0", ec="#E63946", lw=1))
    
    ax.annotate(f'Abandono: {aban_2/s1*100:.1f}%\n({int(aban_2)} no van)', 
                xy=(1.5, (s1 + p2)/2), xytext=(1.5, p1*0.62),
                ha='center', fontsize=8, fontweight='bold', color='#D97706',
                bbox=dict(boxstyle="round,pad=0.2", fc="#FFFBEB", ec="#D97706", lw=1))
    
    ax.annotate(f'Cae: {c2/p2*100:.1f}%\n({int(c2)} susp.)', 
                xy=(2.5, (p2 + s2)/2), xytext=(2.5, p1*0.42),
                ha='center', fontsize=8, fontweight='bold', color='#E63946',
                bbox=dict(boxstyle="round,pad=0.2", fc="#FFF0F0", ec="#E63946", lw=1))

plot_progression_ejercicios(ax1, 2018)
plot_progression_ejercicios(ax2, 2019)

# Panel 3: Convocatoria 2024 (Examen Único: Presentados 1º Ej vs Superan Proceso)
r24 = df_libre[df_libre['convocatoria'] == 2024].iloc[0]
p24 = r24['presentados_1ej_total']
aprob24 = r24['superan_proceso_total']
caen24 = p24 - aprob24
stages_24 = ['1º Ejercicio\n(Presentados)', 'Superan Proceso\n(Aprobados Plaza)', 'No Superan\n(Caen en pruebas)']
vals_24 = [p24, aprob24, caen24]
colors_24 = ['#1D3557', '#2A9D8F', '#E76F51']

bars24 = ax3.bar(stages_24, vals_24, color=colors_24, width=0.55, edgecolor='white', linewidth=1.5)
ax3.set_title(f'Convocatoria 2024 (Examen Único)\nPlazas: 995 | Solicitudes: 2.482', fontsize=11, fontweight='bold', pad=12)
ax3.set_ylabel('Número de Opositores', fontsize=10, fontweight='bold')
ax3.grid(True, alpha=0.3, axis='y')
ax3.set_ylim(0, p24 * 1.25)

for bar in bars24:
    h = bar.get_height()
    pct = h / p24 * 100
    ax3.text(bar.get_x() + bar.get_width()/2., h + (p24*0.02), f'{int(h)}\n({pct:.1f}%)', 
             ha='center', va='bottom', fontsize=9, fontweight='bold')

ax3.annotate(f'Superan: 39.7%\nCaen: 60.3%', xy=(1.5, p24*0.65), xytext=(1.5, p24*0.8),
             ha='center', fontsize=9, fontweight='bold', color='#1D3557',
             bbox=dict(boxstyle="round,pad=0.3", fc="#EAF2F8", ec="#1D3557", lw=1))

plt.suptitle('INGRESO LIBRE: PROGRESIÓN Y CRIBA POR EJERCICIO (2018, 2019 Y 2024)', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('08_ingreso_libre_criba_por_ejercicio.png', dpi=150, bbox_inches='tight')
plt.close()

# ============================================
# 10. GRÁFICO 9: DESTINO DE CANDIDATOS (CONVOCATORIA E HISTÓRICO)
# ============================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

convs = df_libre['convocatoria'].astype(str).tolist()
sol = df_libre['solicitudes_total'].values
pres = df_libre['presentados_1ej_total'].values
aprob = df_libre['superan_proceso_total'].values

no_pres = sol - pres
susp = pres - aprob

pct_aprob = (aprob / sol * 100)
pct_susp = (susp / sol * 100)
pct_no_pres = (no_pres / sol * 100)

w = 0.55
b1 = ax1.bar(x, aprob, w, label='Superan Proceso (Obtienen Plaza)', color='#2A9D8F', alpha=0.9)
b2 = ax1.bar(x, susp, w, bottom=aprob, label='No Superan Examen (Suspensos)', color='#E76F51', alpha=0.85)
b3 = ax1.bar(x, no_pres, w, bottom=aprob + susp, label='No se Presentan (Absentismo Previo)', color='#B0BEC5', alpha=0.7)

ax1.set_title('Destino de los Solicitantes por Convocatoria (Números Absolutos)', fontsize=12, fontweight='bold', pad=12)
ax1.set_xlabel('Convocatoria', fontsize=11, fontweight='bold')
ax1.set_ylabel('Número de Aspirantes', fontsize=11, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(convs, fontsize=10)
ax1.legend(fontsize=9, loc='upper left')
ax1.grid(True, alpha=0.3, axis='y')

for i in range(len(convs)):
    ax1.text(i, sol[i] + 40, f'Total: {sol[i]}\n({pct_aprob[i]:.1f}% con plaza)', 
             ha='center', va='bottom', fontsize=9, fontweight='bold')
    if aprob[i] > 60:
        ax1.text(i, aprob[i]/2, f'{aprob[i]}\n({pct_aprob[i]:.0f}%)', ha='center', va='center', color='white', fontweight='bold', fontsize=8)
    if susp[i] > 100:
        ax1.text(i, aprob[i] + susp[i]/2, f'{susp[i]}\n({pct_susp[i]:.0f}%)', ha='center', va='center', color='white', fontweight='bold', fontsize=8)
    if no_pres[i] > 100:
        ax1.text(i, aprob[i] + susp[i] + no_pres[i]/2, f'{no_pres[i]}\n({pct_no_pres[i]:.0f}%)', ha='center', va='center', color='#263238', fontweight='bold', fontsize=8)

tot_sol = sol.sum()
tot_p1 = pres.sum()
tot_aprob = aprob.sum()
tot_susp = susp.sum()
tot_no_pres = no_pres.sum()

categories = ['Superan Proceso\n(Obtienen Plaza)', 'No Superan Examen\n(Suspensos)', 'No se Presentan\n(Absentismo)']
totals = [tot_aprob, tot_susp, tot_no_pres]
tot_pcts = [tot_aprob/tot_sol*100, tot_susp/tot_sol*100, tot_no_pres/tot_sol*100]
colors_bar = ['#2A9D8F', '#E76F51', '#B0BEC5']

b_hist = ax2.bar(categories, totals, color=colors_bar, width=0.55, edgecolor='white', linewidth=1.5)
ax2.set_title(f'Balance Histórico Acumulado 2018-2024\nTotal Solicitudes: {tot_sol:,}', fontsize=12, fontweight='bold', pad=12)
ax2.set_ylabel('Número Total de Personas', fontsize=11, fontweight='bold')
ax2.grid(True, alpha=0.3, axis='y')
ax2.set_ylim(0, max(totals) * 1.2)

for bar, pct in zip(b_hist, tot_pcts):
    h = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., h + 80, f'{int(h):,} personas\n({pct:.1f}% de solicitudes)',
             ha='center', va='bottom', fontsize=9.5, fontweight='bold')

plt.suptitle('INGRESO LIBRE: ¿QUÉ PASA CON LOS ASPIRANTES? SUPERAN vs CAEN (POR CONVOCATORIA E HISTÓRICO)', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('09_ingreso_libre_destino_candidatos_historico.png', dpi=150, bbox_inches='tight')
plt.close()

# ============================================
# 11. GRÁFICO 10 (NUEVO): BALANCE DE TODAS LAS PLAZAS CONVOCADAS VS DESIERTAS (2024 Y TOTAL)
# ============================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5.5))

# Panel 1: Convocatoria 2024 (Libre, Promo y Total)
cats_2024 = ['Ingreso Libre\n(2024)', 'Promoción Interna\n(2024)', 'TOTAL GSI\n(2024)']
plz_conv_2024 = [995, 800, 1795]
plz_cub_2024 = [410, 162, 572]
plz_des_2024 = [585, 638, 1223]
pct_des_2024 = [585/995*100, 638/800*100, 1223/1795*100]

b_cub_24 = ax1.bar(cats_2024, plz_cub_2024, width=0.55, label='Plazas Cubiertas', color='#2A9D8F', alpha=0.9)
b_des_24 = ax1.bar(cats_2024, plz_des_2024, width=0.55, bottom=plz_cub_2024, label='Plazas Desiertas', color='#E76F51', alpha=0.85)

ax1.set_title('Convocatoria 2024: Plazas Cubiertas vs Desiertas', fontsize=12, fontweight='bold', pad=12)
ax1.set_ylabel('Número de Plazas', fontsize=11, fontweight='bold')
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3, axis='y')
ax1.set_ylim(0, 2200)

for i in range(len(cats_2024)):
    ax1.text(i, plz_conv_2024[i] + 40, f'Convocadas: {plz_conv_2024[i]}\nDesiertas: {plz_des_2024[i]} ({pct_des_2024[i]:.1f}%)',
             ha='center', va='bottom', fontsize=9.5, fontweight='bold', color='#264653')
    ax1.text(i, plz_cub_2024[i]/2, f'{plz_cub_2024[i]}', ha='center', va='center', color='white', fontweight='bold', fontsize=10)
    ax1.text(i, plz_cub_2024[i] + plz_des_2024[i]/2, f'{plz_des_2024[i]}', ha='center', va='center', color='white', fontweight='bold', fontsize=10)

# Panel 2: Evolución de Plazas Desiertas por Convocatoria (Total GSI: Libre + Promo)
conv_all = ['2018', '2019', '2022', '2024']
total_plazas_yr = [358, 480, 1440, 1795]
total_cubiertas_yr = [175, 254, 459, 572]
total_desiertas_yr = [183, 226, 981, 1223]
pct_des_yr = [183/358*100, 226/480*100, 981/1440*100, 1223/1795*100]

b_cub_yr = ax2.bar(conv_all, total_cubiertas_yr, width=0.55, label='Plazas Cubiertas (Total GSI)', color='#2A9D8F', alpha=0.9)
b_des_yr = ax2.bar(conv_all, total_desiertas_yr, width=0.55, bottom=total_cubiertas_yr, label='Plazas Desiertas (Total GSI)', color='#E76F51', alpha=0.85)

ax2.set_title('Evolución Histórica de Plazas Desiertas (Total GSI: Libre + Promo)', fontsize=12, fontweight='bold', pad=12)
ax2.set_xlabel('Convocatoria', fontsize=11, fontweight='bold')
ax2.set_ylabel('Número de Plazas', fontsize=11, fontweight='bold')
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3, axis='y')
ax2.set_ylim(0, 2200)

for i in range(len(conv_all)):
    ax2.text(i, total_plazas_yr[i] + 40, f'{total_desiertas_yr[i]} desiertas\n({pct_des_yr[i]:.1f}%)',
             ha='center', va='bottom', fontsize=9.5, fontweight='bold', color='#E63946')
    ax2.text(i, total_cubiertas_yr[i]/2, f'{total_cubiertas_yr[i]}', ha='center', va='center', color='white', fontweight='bold', fontsize=9)
    ax2.text(i, total_cubiertas_yr[i] + total_desiertas_yr[i]/2, f'{total_desiertas_yr[i]}', ha='center', va='center', color='white', fontweight='bold', fontsize=9)

plt.suptitle('RADIOGRAFÍA DE PLAZAS DESIERTAS: EN 2024 EL 68.1% DE LAS PLAZAS QUEDARON VACÍAS', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('10_resumen_plazas_desiertas_todas.png', dpi=150, bbox_inches='tight')
plt.close()

# ============================================
# 12. RESUMEN EJECUTIVO EN CONSOLA
# ============================================
print("\n" + "="*80)
print("INFORME ESTADÍSTICO AUDITADO Y VERIFICADO - GSI AGE (2018-2024)")
print("="*80)

print("\n📊 1. CONVOCATORIA 2024 - PRESENTADOS 1º EJERCICIO vs SUPERAN PROCESO COMPLETO:")
print(f"   • INGRESO LIBRE TOTAL: 1.033 se presentaron al 1er Ejercicio.")
print(f"     - Superan el proceso completo: 410 (39.69% de los presentados)")
print(f"     - No superan / Caen en las pruebas: 623 (60.31% de los presentados)")
print(f"     - Cupo General: 1.004 presentados -> 397 superan (39.54%) | 607 caen (60.46%)")
print(f"     - Cupo Discapacidad (CRD): 29 presentados -> 13 superan (44.83%) | 16 caen (55.17%)")
print(f"   • PROMOCIÓN INTERNA TOTAL: 186 se presentaron al 1er Ejercicio.")
print(f"     - Superan el proceso completo: 162 (87.10% de los presentados)")
print(f"     - No superan / Caen: 24 (12.90% de los presentados)")
print(f"   • TOTAL GSI 2024: 1.219 se presentaron al 1er Ejercicio.")
print(f"     - Superan el proceso completo: 572 (46.92% de los presentados)")
print(f"     - No superan / Caen: 647 (53.08% de los presentados)")

print("\n📉 2. PLAZAS DESIERTAS CONVOCATORIA 2024 (DE TODAS LAS CONVOCADAS ESE AÑO):")
print(f"   • INGRESO LIBRE 2024:")
print(f"     - Plazas convocadas: 995 (General: 937, Discapacidad: 58)")
print(f"     - Plazas cubiertas: 410 (General: 397, Discapacidad: 13)")
print(f"     - PLAZAS DESIERTAS: 585 plazas desiertas (58.79% sin cubrir)")
print(f"       * Cupo General: 540 plazas desiertas de 937 (57.63%)")
print(f"       * Cupo Discapacidad: 45 plazas desiertas de 58 (77.59%)")
print(f"   • PROMOCIÓN INTERNA 2024:")
print(f"     - Plazas convocadas: 800 (General: 754, Discapacidad: 46)")
print(f"     - Plazas cubiertas: 162 (General: 155, Discapacidad: 7)")
print(f"     - PLAZAS DESIERTAS: 638 plazas desiertas (79.75% sin cubrir)")
print(f"   • TOTAL GSI 2024 (Libre + Promo):")
print(f"     - Plazas convocadas: 1.795 plazas")
print(f"     - Plazas cubiertas: 572 plazas")
print(f"     - TOTAL PLAZAS DESIERTAS 2024: ¡1.223 PLAZAS DESIERTAS (el 68.13% de todas las plazas convocadas)!")

print("\n🏛️ 3. TOTAL HISTÓRICO ACUMULADO (2018-2024):")
print(f"   • Ingreso Libre: 1.320 plazas desiertas de 2.333 convocadas (56.58% desiertas)")
print(f"   • Promoción Interna: 1.293 plazas desiertas de 1.740 convocadas (74.31% desiertas)")
print(f"   • TOTAL GSI HISTÓRICO: 2.613 plazas desiertas de 4.073 convocadas (64.15% desiertas)")

print("\n" + "="*80)
print("✅ Todos los gráficos actualizados y guardados como PNG:")
print("   - 01_tasa_exito.png")
print("   - 02_competitividad.png")
print("   - 03_plazas_vs_aprobados.png")
print("   - 04_embudo_conversion.png")
print("   - 05_tasa_presentacion.png")
print("   - 06_ingreso_libre_general_vs_discapacidad.png")
print("   - 07_ingreso_libre_oeps_acumuladas.png")
print("   - 08_ingreso_libre_criba_por_ejercicio.png")
print("   - 09_ingreso_libre_destino_candidatos_historico.png")
print("   - 10_resumen_plazas_desiertas_todas.png  (NUEVO)")
print("="*80)
