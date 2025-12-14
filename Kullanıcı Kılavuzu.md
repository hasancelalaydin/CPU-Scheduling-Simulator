# CPU Zamanlama Programı

Bu proje, İşletim Sistemleri dersinde verilen CPU Zamanlama ödevi için geliştirilmiştir.

## Desteklenen Algoritmalar
- FCFS (First Come First Served)
- SJF (Non-Preemptive)
- SJF (Preemptive / SRTF)
- Round Robin (Quantum = 4)
- Priority Scheduling (Non-Preemptive)
- Priority Scheduling (Preemptive)

## Giriş Dosyaları
CSV formatında süreç bilgileri:
- Process_ID
- Arrival_Time
- CPU_Burst_Time
- Priority (high, normal, low)

## Sonuç 
Bu kılavuz, proje hakkında bilgi vermek amacıyla 
hazırlanmıştır. Program tüm algoritmaları otomatik olarak çalıştırıp çıktı 
oluşturabilmektedir.

## Çalıştırma
```bash
cd src
python main.py
