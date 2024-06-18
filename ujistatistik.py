import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Membaca data dari file CSV dengan delimiter ';'
df = pd.read_csv('pengangguran.csv', delimiter=';')

# Cetak nama kolom untuk memastikan kolom dibaca dengan benar
print(df.columns)

# Menghapus spasi ekstra di sekitar nama kolom dan baris
df.columns = df.columns.str.strip()
df['Golongan Umur'] = df['Golongan Umur'].str.strip()

# Menampilkan nama kolom untuk memastikan kolom sudah bersih
print(df.columns)

# Menampilkan 10 baris pertama dari data
print(df.head(10))

# Mengganti titik dengan kosong untuk konversi ke integer
df.replace({'\.': '', ',': ''}, regex=True, inplace=True)

# Mengonversi data menjadi integer, kecuali kolom pertama
for col in df.columns[1:]:
    df[col] = df[col].astype(int)

# Menghitung persentase pengangguran
total_pengangguran = df.loc[df['Golongan Umur'] == 'Total angka pengangguran'].values[0][1:]
jumlah_angkatan_kerja = df.loc[df['Golongan Umur'] == 'Jumlah angkatan kerja'].values[0][1:]

persentase_pengangguran = (total_pengangguran / jumlah_angkatan_kerja) * 100

# Membuat DataFrame baru untuk persentase pengangguran
periode = df.columns[1:]
persentase_df = pd.DataFrame({
    'Periode': periode,
    'Persentase Pengangguran': persentase_pengangguran
})

# Visualisasi persentase pengangguran dengan gaya yang lebih menarik
plt.figure(figsize=(14, 7))
plt.plot(periode, persentase_pengangguran, marker='o', color='#ffa600', linestyle='-', linewidth=2, markersize=8)
plt.xlabel('Periode')
plt.ylabel('Persentase Pengangguran (%)')
plt.title('Persentase Pengangguran terhadap Jumlah Angkatan Kerja (2019-2023)')
plt.xticks(rotation=45)
plt.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray')
plt.tight_layout()
plt.show()

# Visualisasi Tren Waktu
plt.figure(figsize=(14, 7))
for age_group in df['Golongan Umur'][:-1]:  # Exclude 'Total'
    plt.plot(df.columns[1:], df.loc[df['Golongan Umur'] == age_group].values.flatten()[1:], label=age_group) 

plt.xlabel('Periode')
plt.ylabel('Jumlah Pengangguran')
plt.title('Tren Pengangguran per Golongan Umur (2019-2023)')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Mengecualikan baris 'Total angka pengangguran' dan 'Jumlah angkatan kerja' dari perbandingan
df_comparison = df[(df['Golongan Umur'] != 'Total angka pengangguran') & (df['Golongan Umur'] != 'Jumlah angkatan kerja')]

# Mengubah format data untuk perbandingan antar tahun
comparison = df_comparison.set_index('Golongan Umur').T

# Menampilkan perbandingan data dalam bentuk bar plot
comparison.plot(kind='bar', figsize=(14, 7))
plt.title('Perbandingan Pengangguran per Tahun dan Kelompok Umur')
plt.xlabel('Periode')
plt.ylabel('Jumlah Pengangguran')
plt.legend(title='Golongan Umur')
plt.xticks(rotation=45)
plt.tight_layout()
plt.grid(True)
plt.show()

# Visualisasi Perbandingan Antar Kelompok Umur untuk Setiap Periode
for period in df.columns[1:]:
    plt.figure(figsize=(10, 5))
    bars = plt.bar(df['Golongan Umur'].iloc[:-2], df[period].iloc[:-2],
                   color=['#ffb400', '#d2980d', '#a57c1b', '#786028', '#363445', '#48446e', '#5e569b', '#776bcd', '#9080ff', '#a4a2a8'])  # Exclude rows 12 and 13
    plt.xlabel('Golongan Umur')
    plt.ylabel('Jumlah Pengangguran')
    plt.title(f'Perbandingan Pengangguran per Golongan Umur - {period}')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Misalkan Anda sudah melakukan filter df untuk membuat df_filtered
rows_to_exclude = ['Total angka pengangguran', 'Jumlah angkatan kerja']
df_filtered = df[~df['Golongan Umur'].isin(rows_to_exclude)]

# Menghitung pertumbuhan/pemurunan persentase pengangguran
growth = df_filtered.set_index('Golongan Umur').pct_change(axis='columns') * 100

# Membuat diagram polar area
fig = go.Figure()

for column in growth.columns:
    fig.add_trace(go.Scatterpolar(
        r=growth[column],
        theta=growth.index,
        fill='toself',
        name=column
    ))

# Menyesuaikan layout
fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, growth.max().max()],  # Range radial axis sesuaikan dengan data maksimal
        )),
    title='Pertumbuhan/Penurunan Persentase Pengangguran per Golongan Umur',
    showlegend=True
)

# Menampilkan diagram polar area
fig.show()

# Statistik Deskriptif
descriptive_stats = df.describe()
print(descriptive_stats)

# Kecualikan baris 12 dan 13
df_filtered = df.iloc[:-2]

# Plot Statistik Deskriptif
df.describe().plot(kind='bar', figsize=(14, 7))
plt.title('Statistik Deskriptif Pengangguran per Golongan Umur')
plt.xlabel('Statistik')
plt.ylabel('Jumlah')
plt.legend(title='Golongan Umur')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
