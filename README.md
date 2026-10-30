# CPU Zamanlama Simülatörü

İşletim Sistemleri dersi ödevi için Python ile yaptığım bir proje.
Altı CPU zamanlama algoritmasını iki farklı proses kümesi üzerinde çalıştırıp sonuçlarını karşılaştırdım.

Denenen algoritmalar: FCFS, SJF (kesmeli ve kesmesiz), Round Robin (q=4), Priority (kesmeli ve kesmesiz).

Her algoritma için bekleme süresi, turnaround süresi, throughput, bağlam değiştirme sayısı ve CPU verimliliği hesaplanıyor.
Denemelerde ortalama bekleme ve turnaround süresinde genellikle en iyi sonucu kesmeli SJF verdi.

Sonuçlar `Odev1_*` dosyalarında, yorumlar ise `Proje Raporu.md` dosyasında.
