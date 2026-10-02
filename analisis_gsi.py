import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configurar estilo
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

# ============================================
# 1. DATOS
# ============================================

datos = {
    'convocatoria': ['2018', '2019', '2022', '2024'],
    'plazas_libre': [218, 280, 840, 995],
    'plazas_promo': [140, 200, 600, 800],
    'solicitudes_libre': [2087, 1574, 2437, 2482],
    'solicitudes_promo': [196, 309, 466, 385],
    'presentados_libre': [1027, 719, 1488, 1219],
    'presentados_promo': [176, 223, 269, 186],
    'aprobados_libre': [144, 143, 459, 572],
    'aprobados_promo': [31, 111, 143, 162],
    'tasa_exito_libre': [14.02, 19.89, 30.85, 46.92],
    'tasa_exito_promo': [17.61, 49.78, 53.16, 87.10],
    'ratio_libre': [9.57, 5.62, 2.90, 2.49],
    'ratio_promo': [1.40, 1.54, 0.78, 0.48],
}

df = pd.DataFrame(datos)
df['tasa_presentacion_libre'] = (df['presentados_libre'] / df['solicitudes_libre'] * 100).round(2)
df['tasa_presentacion_promo'] = (df['presentados_promo'] / df['solicitudes_promo'] * 100).round(2)

print("✅ Datos cargados correctamente")
print(f"Convocatorias analizadas: {df['convocatoria'].tolist()}")

# ============================================
# 2. GRÁFICO 1: EVOLUCIÓN TASA DE ÉXITO
# ============================================

fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(df['convocatoria'], df['tasa_exito_libre'], 'o-', linewidth=3, markersize=10, 
        label='Ingreso Libre', color='#2E86AB', markeredgecolor='white', markeredgewidth=2)
ax.plot(df['convocatoria'], df['tasa_exito_promo'], 's-', linewidth=3, markersize=10, 
        label='Promoción Interna', color='#A23B72', markeredgecolor='white', markeredgewidth=2)

ax.set_xlabel('Convocatoria', fontsize=14, fontweight='bold')
ax.set_ylabel('Tasa de Éxito Global (%)', fontsize=14, fontweight='bold')
ax.set_title('EVOLUCIÓN TASA DE ÉXITO (2018-2024)\n% de presentados que aprueban todo el proceso', 
             fontsize=16, fontweight='bold', pad=20)
ax.legend(fontsize=12, loc='upper left')
ax.grid(True, alpha=0.3)
ax.set_ylim(0, 100)

# Añadir etiquetas con valores
for i, (v1, v2) in enumerate(zip(df['tasa_exito_libre'], df['tasa_exito_promo'])):
    ax.text(i, v1+3, f'{v1:.1f}%', ha='center', fontsize=11, fontweight='bold', color='#2E86AB')
    ax.text(i, v2+3, f'{v2:.1f}%', ha='center', fontsize=11, fontweight='bold', color='#A23B72')

plt.tight_layout()
plt.savefig('01_tasa_exito.png', dpi=150, bbox_inches='tight')
plt.show()

# ============================================
# 3. GRÁFICO 2: COMPETITIVIDAD
# ============================================

fig, ax = plt.subplots(figsize=(12, 6))

x = np.arange(len(df))
width = 0.35

bars1 = ax.bar(x - width/2, df['ratio_libre'], width, label='Ingreso Libre', 
               color='#2E86AB', alpha=0.8, edgecolor='white', linewidth=2)
bars2 = ax.bar(x + width/2, df['ratio_promo'], width, label='Promoción Interna', 
               color='#A23B72', alpha=0.8, edgecolor='white', linewidth=2)

ax.set_xlabel('Convocatoria', fontsize=14, fontweight='bold')
ax.set_ylabel('Opositores por Plaza', fontsize=14, fontweight='bold')
ax.set_title('COMPETITIVIDAD: RATIO OPOSITORES/PLAZA\nMenos es mejor (menos competencia)', 
             fontsize=16, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(df['convocatoria'], fontsize=12)
ax.legend(fontsize=12)
ax.grid(True, alpha=0.3, axis='y')

# Añadir etiquetas
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.2,
                f'{height:.2f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('02_competitividad.png', dpi=150, bbox_inches='tight')
plt.show()

# ============================================
# 4. GRÁFICO 3: PLAZAS vs APROBADOS (COMPARATIVA)
# ============================================

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Ingreso Libre
x = np.arange(len(df))
width = 0.6

aprobados_libre = df['aprobados_libre'].values
desiertas_libre = df['plazas_libre'].values - df['aprobados_libre'].values

ax1.bar(x, aprobados_libre, width, label='Aprobados', color='#06A77D', alpha=0.9, edgecolor='white')
ax1.bar(x, desiertas_libre, width, bottom=aprobados_libre, label='Desiertas', 
        color='#E63946', alpha=0.7, edgecolor='white')

ax1.set_xlabel('Convocatoria', fontsize=12, fontweight='bold')
ax1.set_ylabel('Número de Plazas', fontsize=12, fontweight='bold')
ax1.set_title('INGRESO LIBRE: PLAZAS vs APROBADOS', fontsize=14, fontweight='bold', pad=15)
ax1.set_xticks(x)
ax1.set_xticklabels(df['convocatoria'], fontsize=11)
ax1.legend(fontsize=11)
ax1.grid(True, alpha=0.3, axis='y')

# Añadir etiquetas
for i, (p, a) in enumerate(zip(df['plazas_libre'], df['aprobados_libre'])):
    ax1.text(i, p+40, f'{int(p)}', ha='center', fontsize=10, fontweight='bold')
    ax1.text(i, a/2, f'{int(a)}', ha='center', fontsize=10, color='white', fontweight='bold')

# Promoción Interna
aprobados_promo = df['aprobados_promo'].values
desiertas_promo = df['plazas_promo'].values - df['aprobados_promo'].values

ax2.bar(x, aprobados_promo, width, label='Aprobados', color='#06A77D', alpha=0.9, edgecolor='white')
ax2.bar(x, desiertas_promo, width, bottom=aprobados_promo, label='Desiertas', 
        color='#E63946', alpha=0.7, edgecolor='white')

ax2.set_xlabel('Convocatoria', fontsize=12, fontweight='bold')
ax2.set_ylabel('Número de Plazas', fontsize=12, fontweight='bold')
ax2.set_title('PROMOCIÓN INTERNA: PLAZAS vs APROBADOS', fontsize=14, fontweight='bold', pad=15)
ax2.set_xticks(x)
ax2.set_xticklabels(df['convocatoria'], fontsize=11)
ax2.legend(fontsize=11)
ax2.grid(True, alpha=0.3, axis='y')

# Añadir etiquetas
for i, (p, a) in enumerate(zip(df['plazas_promo'], df['aprobados_promo'])):
    ax2.text(i, p+50, f'{int(p)}', ha='center', fontsize=10, fontweight='bold')
    ax2.text(i, a/2, f'{int(a)}', ha='center', fontsize=10, color='white', fontweight='bold')

plt.tight_layout()
plt.savefig('03_plazas_vs_aprobados.png', dpi=150, bbox_inches='tight')
plt.show()

# ============================================
# 5. GRÁFICO 4: EMBUDO DE CONVERSIÓN
# ============================================

fig, ax = plt.subplots(figsize=(14, 7))

etapas = ['Solicitudes', 'Presentados\n1er Ej.', 'Aprobados\n1er Ej.', 'Aprobados\nProceso']
x_embudo = np.arange(len(etapas))

# Datos 2022 (año con datos más completos)
valores_libre_2022 = [2437, 1488, 459, 459]
valores_promo_2022 = [466, 269, 143, 143]

width = 0.35

bars1 = ax.bar(x_embudo - width/2, valores_libre_2022, width, label='Ingreso Libre (2022)', 
               color='#2E86AB', alpha=0.8, edgecolor='white', linewidth=2)
bars2 = ax.bar(x_embudo + width/2, valores_promo_2022, width, label='Promoción Interna (2022)', 
               color='#A23B72', alpha=0.8, edgecolor='white', linewidth=2)

ax.set_xlabel('Etapa del Proceso Selectivo', fontsize=13, fontweight='bold')
ax.set_ylabel('Número de Opositores', fontsize=13, fontweight='bold')
ax.set_title('EMBUDO DE CONVERSIÓN - CONVOCATORIA 2022\nCaída de candidatos por etapa', 
             fontsize=15, fontweight='bold', pad=20)
ax.set_xticks(x_embudo)
ax.set_xticklabels(etapas, fontsize=11)
ax.legend(fontsize=12)
ax.grid(True, alpha=0.3, axis='y')
ax.set_yscale('log')

# Añadir etiquetas con valores
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height * 1.2,
                f'{int(height)}', ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('04_embudo_conversion.png', dpi=150, bbox_inches='tight')
plt.show()

# ============================================
# 6. GRÁFICO 5: TASA DE PRESENTACIÓN
# ============================================

fig, ax = plt.subplots(figsize=(12, 6))

x = np.arange(len(df))
width = 0.35

bars1 = ax.bar(x - width/2, df['tasa_presentacion_libre'], width, 
               label='Ingreso Libre', color='#2E86AB', alpha=0.8, edgecolor='white', linewidth=2)
bars2 = ax.bar(x + width/2, df['tasa_presentacion_promo'], width, 
               label='Promoción Interna', color='#A23B72', alpha=0.8, edgecolor='white', linewidth=2)

ax.set_xlabel('Convocatoria', fontsize=14, fontweight='bold')
ax.set_ylabel('Tasa de Presentación (%)', fontsize=14, fontweight='bold')
ax.set_title('TASA DE PRESENTACIÓN\n% de solicitantes que realmente se presentan al examen', 
             fontsize=16, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(df['convocatoria'], fontsize=12)
ax.legend(fontsize=12)
ax.set_ylim(0, 100)
ax.grid(True, alpha=0.3, axis='y')

# Añadir etiquetas
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 2,
                f'{height:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('05_tasa_presentacion.png', dpi=150, bbox_inches='tight')
plt.show()

# ============================================
# 7. RESUMEN DE HALLAZGOS
# ============================================

print("\n" + "="*80)
print("RESUMEN DE HALLAZGOS CLAVE")
print("="*80)

print("\n📊 TASA DE ÉXITO GLOBAL (2024):")
print(f"   • Ingreso Libre: {df['tasa_exito_libre'].iloc[-1]:.1f}% (mejora de {df['tasa_exito_libre'].iloc[0]:.1f}% en 2018)")
print(f"   • Promoción Interna: {df['tasa_exito_promo'].iloc[-1]:.1f}% (mejora de {df['tasa_exito_promo'].iloc[0]:.1f}% en 2018)")

print("\n🎯 COMPETITIVIDAD (2024):")
print(f"   • Ingreso Libre: {df['ratio_libre'].iloc[-1]:.2f} opositores/plaza")
print(f"   • Promoción Interna: {df['ratio_promo'].iloc[-1]:.2f} opositores/plaza (<1!)")

print("\n📉 PLAZAS DESIERTAS (2024):")
desiertas_libre_2024 = df['plazas_libre'].iloc[-1] - df['aprobados_libre'].iloc[-1]
desiertas_promo_2024 = df['plazas_promo'].iloc[-1] - df['aprobados_promo'].iloc[-1]
print(f"   • Ingreso Libre: {int(desiertas_libre_2024)} plazas sin cubrir ({df['plazas_libre'].iloc[-1] - df['aprobados_libre'].iloc[-1]}/{df['plazas_libre'].iloc[-1]})")
print(f"   • Promoción Interna: {int(desiertas_promo_2024)} plazas sin cubrir ({df['plazas_promo'].iloc[-1] - df['aprobados_promo'].iloc[-1]}/{df['plazas_promo'].iloc[-1]})")

print("\n💡 CONCLUSIÓN:")
print("   • Promoción Interna es MUCHO más accesible (menos competencia, más tasa de éxito)")
print("   • Ingreso Libre ha mejorado significativamente pero sigue siendo competitivo")
print("   • Ambas modalidades tienen muchas plazas desiertas en convocatorias acumuladas")

print("\n" + "="*80)
print("✅ Todos los gráficos se han guardado como archivos PNG")
print("   - 01_tasa_exito.png")
print("   - 02_competitividad.png")
print("   - 03_plazas_vs_aprobados.png")
print("   - 04_embudo_conversion.png")
print("   - 05_tasa_presentacion.png")
print("="*80)
