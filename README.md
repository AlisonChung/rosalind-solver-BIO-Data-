# 🧬 Rosalind Solver — BIO Data

DNA 서열 분석 프로그램입니다.  
파일(.txt / .pdf)을 업로드하면 **염기 개수 세기**와 **RNA 전사** 결과를 바로 확인할 수 있어요.

---

## 📋 기능

| 기능 | 설명 |
|---|---|
| 염기 개수 세기 | A, C, G, T 각각의 개수 + GC 함량(%) 계산 |
| RNA 전사 | DNA 서열의 T를 U로 변환한 RNA 서열 생성 |
| 복사용 한 줄 출력 | `A개수 C개수 G개수 T개수` 형식으로 한 번에 복사 |
| 파일 업로드 | `.txt` / `.pdf` / FASTA 형식 모두 지원 |

---

## 🗂️ 파일 구조

```
rosalind-solver-BIO-Data/
├── app.py            # Streamlit 웹앱 (브라우저에서 사용)
├── dna_analyzer.py   # CLI 프로그램 (터미널에서 사용)
└── requirements.txt  # 필요한 패키지 목록
```

---

## 🚀 실행 방법

### 1. 패키지 설치 (처음 한 번만)

```bash
pip install streamlit pdfplumber
```

### 2-A. 웹앱으로 실행 (추천)

```bash
streamlit run app.py
```

브라우저에서 `http://localhost:8501` 자동으로 열림  
→ 파일 업로드하면 결과 바로 확인 가능

### 2-B. 터미널에서 실행

```bash
# 서열 직접 입력
python dna_analyzer.py --seq ATAGATCACGTAGT

# 파일로 입력
python dna_analyzer.py --file my_sequence.txt
```

---

## 📊 출력 예시

**입력:** `ATAGATCACGTAGT`

```
[ Counting DNA Nucleotides ]
  A = 5
  C = 2
  G = 3
  T = 4
  GC 함량 = 35.71%

[ Transcribing DNA into RNA ]
  AUAGAUCACGUAGU
```

---

## 🔬 지원 입력 형식

**일반 텍스트 (.txt)**
```
ATAGATCACGTAGT
```

**FASTA 형식 (.txt / .pdf)**
```
>Rosalind_001
ATAGATCACGTAGT
```

> FASTA 헤더(`>`로 시작하는 줄)는 자동으로 제거되고 서열만 분석합니다.

---

## 🧩 로잘린드(Rosalind)란?

[Rosalind](https://rosalind.info)는 생물정보학 문제를 코딩으로 풀어보는 온라인 플랫폼입니다.  
이 프로그램은 로잘린드의 아래 문제를 다룹니다:

- **DNA** — [Counting DNA Nucleotides](https://rosalind.info/problems/dna/)
- **RNA** — [Transcribing DNA into RNA](https://rosalind.info/problems/rna/)
