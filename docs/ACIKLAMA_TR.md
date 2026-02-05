# Pentrex — Türkçe Açıklama

Siber güvenlik öğrenimi için AI agent. CEH ve pentest konularını quiz, açıklama ve senaryo modlarıyla öğreniyorsun.

---

## Proje Yapısı

```
pentrex/
├── pentrex/
│   ├── loop.py           # Agent döngüsü (beyin)
│   ├── config.py         # Ayarlar
│   └── tools/
│       ├── registry.py   # Tool kayıt sistemi
│       ├── quiz.py       # Quiz soruları
│       ├── explain.py    # Kavram açıklamaları
│       ├── toolguide.py  # Pentest araç rehberi
│       └── scenario.py   # Saldırı senaryoları
├── examples/
│   └── chat.py           # İnteraktif sohbet
└── tests/
    └── test_tools.py     # Testler
```

---

## Ne Yapıyor?

### 1. Quiz Modu (`quiz.py`)

7 farklı domain'den sorular:
- **reconnaissance** — Keşif teknikleri
- **scanning** — Port ve zafiyet tarama
- **system_hacking** — Sistem ele geçirme
- **web_attacks** — Web saldırıları (SQLi, XSS)
- **network_attacks** — Ağ saldırıları (ARP Spoofing, MitM)
- **wireless** — Kablosuz güvenlik
- **cryptography** — Şifreleme

Her soru 4 şık, doğru cevap ve açıklama içeriyor.

### 2. Açıklama Modu (`explain.py`)

Güvenlik kavramlarının detaylı açıklaması:
- SQL Injection nasıl çalışır
- XSS türleri neler
- Buffer Overflow nedir
- Önleme yöntemleri neler

### 3. Araç Rehberi (`toolguide.py`)

8 popüler pentest aracı:
- **Nmap** — Port tarama
- **Metasploit** — Exploitation framework
- **Burp Suite** — Web testi
- **Wireshark** — Paket analizi
- **sqlmap** — SQL injection otomasyonu
- **Hydra** — Brute force
- **Aircrack-ng** — Wireless
- **John the Ripper** — Hash cracking

Her araç için: açıklama, flagler, örnek komutlar.

### 4. Senaryo Modu (`scenario.py`)

Pratik saldırı senaryoları:
- Web SQL Injection (Beginner)
- ARP Spoofing (Intermediate)
- WPA2 Handshake Cracking (Intermediate)
- Linux Privilege Escalation (Advanced)

Her senaryo: hedef, araçlar, adım adım komutlar, öğrenilen dersler.

---

## Agent Loop Nasıl Çalışıyor?

`loop.py` agent-101'deki gibi çalışıyor:

1. Kullanıcı mesaj yazar
2. Claude API'ye gönderilir (tools + history)
3. Claude tool çağırırsa → tool çalışır, sonuç geri gider
4. Claude cevap verirse → ekrana yazdırılır

Fark: Burada 4 farklı tool var, Claude soruya göre hangisini çağıracağına karar veriyor.

---

## Örnek Kullanım

```
you > quiz me on web attacks

pentrex > [get_quiz_question çağırır]

Which attack injects malicious scripts into web pages?
A) SQL Injection
B) XSS
C) CSRF
D) Directory Traversal

you > b

pentrex > Correct! Cross-Site Scripting (XSS) injects malicious 
scripts that execute in victims' browsers...
```

```
you > explain sql injection

pentrex > [explain_concept çağırır]

SQL Injection is a code injection technique...
How it works:
1. Application takes user input...
2. Input isn't sanitized...
Prevention: Use parameterized queries...
```

```
you > show me nmap examples

pentrex > [get_tool_guide çağırır]

Common flags:
  -sS: TCP SYN scan (stealth)
  -sV: Service version detection
  
Examples:
  nmap -sS -sV -p- 192.168.1.1
  nmap --script vuln 192.168.1.1
```

---

## Nasıl Katkı Yapılır?

Bu alanlar yardım bekliyor:

1. **Daha fazla quiz sorusu** — `quiz.py`'ye ekle
2. **Yeni kavramlar** — `explain.py`'ye ekle
3. **Başka araçlar** — `toolguide.py`'ye ekle (Nikto, Dirb, Gobuster vs.)
4. **Yeni senaryolar** — `scenario.py`'ye ekle

Format basit — dictionary'ye yeni entry eklemen yeterli.

---

## Çalıştırma

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY="your-key"
python -m examples.chat
```

Ya da test için (API key gerekmez):

```bash
python -m tests.test_tools
```
