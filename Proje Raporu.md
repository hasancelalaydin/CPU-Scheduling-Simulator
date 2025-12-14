İŞLETİM SİSTEMLERİ ÖDEVİ  
CPU Zamanlama Algoritmaları Performans Analizi Raporu  


ÖĞRENCİ ADI SOYADI: Hasan Celal Aydın 
ÖĞRENCİ NUMARASI: 20232013038 

 

Giriş  

Bu rapor, verilen iki farklı proses kümesi (Case 1 ve Case 2) üzerinde altı CPU zamanlama algoritmasının performans karşılaştırmasını sunmaktadır. Her algoritma için bekleme süreleri, turnaround süreleri, throughput değerleri, bağlam değiştirme sayıları ve CPU verimliliği hesaplanmıştır.  

Algoritmalar:  

First Come First Served (FCFS)  

Non-Preemptive SJF  

Preemptive SJF (SRTF)  

Round Robin (quantum = 4)  

Non-Preemptive Priority  

Preemptive Priority 

 

Veri Setlerinin Özeti 

 Case 1  

100 prosesten oluşmaktadır. Arrival time değerleri 0–198 aralığında, burst süreleri 1 20 aralığındadır. Öncelikler “high”, “normal” ve “low” olarak verilmiştir.  
(Veri kaynağı: Odev1_Case1.txt)  

Case 2  
200’den fazla proses içerir. Daha geniş zaman aralıklarında arrival time ve burst time değerleri vardır. (Veri kaynağı: Odev1_case2.txt) Her iki veri seti de CPU zamanlama algoritmalarının farklı yük seviyelerinde davranışını incelemek için uygundur. 

 

Kullanılan Algoritmaların Özeti  

FCFS  
Prosesler varış sırasına göre çalıştırılır. Preemption yoktur.  


SJF Non-Preemptive  
Hazır kuyruktaki en kısa burst süresine sahip proses seçilir.  
 

SJF Preemptive (SRTF)  
Her zaman remaining time’ı en kısa olan proses çalışır. En fazla context switch oluşan yöntemlerden biridir.  
 

Round Robin (q = 4) 
Her prosese eşit zaman dilimi verilir. Preemptive bir algoritmadır. 


Priority Non-Preemptive  
Öncelik seviyesi yüksek olan (1 = high) proses seçilir.  

 

Priority Preemptive  
CPU’da çalışan proses, daha yüksek öncelikli bir proses gelirse kesilir. 

 
 
Değerlendirme ve Yorumlar  

  SJF Preemptive, ortalama bekleme süresi ve ortalama turnaround süresi açısından genellikle en iyi sonuçları vermiştir.  

  FCFS, prosesler uzun burst sürelerine sahipse yüksek bekleme sürelerine neden olmuştur.  

  Round Robin, fairness sağlar ancak quantum küçük olduğunda context switch sayısını artırır.  

  Priority Preemptive, düşük öncelikli proseslerin starvation yaşamasına neden olabilir.  

  Case 2 veri kümesi daha yoğun olduğundan tüm algoritmalarda context switch sayısı ve toplam süreler artmıştır.  



Sonuç  

CPU zamanlama algoritmalarının performansı proses yapısına, arrival time dağılımına, burst sürelerine ve preemption kullanımına göre büyük farklılık göstermektedir. 
Bu çalışmada altı algoritmanın detaylı karşılaştırması yapılmış ve her yöntemin avantajları ile dezavantajları pratik olarak gözlemlenmiştir. 

 
