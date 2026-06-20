"""
DNA Analyzer — Counting Nucleotides & Transcribing to RNA
사용법:
  python dna_analyzer.py --seq ATAGATCACGTAGT
  python dna_analyzer.py --file my_sequence.txt
"""
import argparse
import os
import sys
import io

# Windows 콘솔 한글 출력 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


def count_nucleotides(sequence):
    A = C = G = T = 0
    unknown = []
    for base in sequence:
        if   base == 'A': A += 1
        elif base == 'C': C += 1
        elif base == 'G': G += 1
        elif base == 'T': T += 1
        else:
            unknown.append(base)
    return A, C, G, T, unknown


def transcribe_to_rna(sequence):
    return sequence.replace('T', 'U')


def analyze(sequence):
    sequence = sequence.strip().upper()

    if not sequence:
        print("오류: 서열이 비어 있어요.")
        sys.exit(1)

    print("=" * 50)
    print(f"  입력 서열 ({len(sequence)}bp)")
    print("=" * 50)
    print(f"  {sequence[:80]}{'...' if len(sequence) > 80 else ''}")
    print()

    # ── 1. Counting DNA Nucleotides ─────────────────
    A, C, G, T, unknown = count_nucleotides(sequence)
    total = A + C + G + T
    gc = (G + C) / total * 100 if total > 0 else 0

    print("[ Counting DNA Nucleotides ]")
    print(f"  A = {A}")
    print(f"  C = {C}")
    print(f"  G = {G}")
    print(f"  T = {T}")
    print(f"  GC 함량 = {gc:.2f}%")
    if unknown:
        unique = sorted(set(unknown))
        print(f"  ⚠ 인식 불가 염기: {', '.join(unique)} (총 {len(unknown)}개 — 계산에서 제외됨)")
    print()

    # ── 2. Transcribing DNA into RNA ────────────────
    rna = transcribe_to_rna(sequence)
    print("[ Transcribing DNA into RNA ]")
    print(f"  {rna[:80]}{'...' if len(rna) > 80 else ''}")
    print()

    # 긴 서열이면 전체 출력 파일 저장
    if len(sequence) > 80:
        out_path = "dna_result.txt"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(f"입력 서열 ({len(sequence)}bp):\n{sequence}\n\n")
            f.write(f"A={A}  C={C}  G={G}  T={T}  GC={gc:.2f}%\n\n")
            f.write(f"RNA 서열 ({len(rna)}bp):\n{rna}\n")
        print(f"  → 전체 결과가 '{out_path}' 파일로 저장됐어요.")
    print("=" * 50)


def main():
    parser = argparse.ArgumentParser(
        description="DNA 염기 개수 세기 + RNA 전사 프로그램"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--seq",  metavar="서열",    help="DNA 서열 직접 입력 (예: ATCGATCG)")
    group.add_argument("--file", metavar="파일경로", help="서열이 담긴 텍스트 파일 경로")
    args = parser.parse_args()

    if args.seq:
        analyze(args.seq)

    elif args.file:
        path = args.file
        if not os.path.exists(path):
            print(f"오류: 파일을 찾을 수 없어요 → {path}")
            sys.exit(1)
        with open(path, "r", encoding="utf-8-sig") as f:
            raw = f.read()

        # FASTA 파일이면 헤더 줄 제거, 나머지 서열 이어붙이기
        if raw.lstrip().startswith(">"):
            lines = raw.splitlines()
            seq_lines = [l for l in lines if not l.startswith(">")]
            sequence = "".join(seq_lines)
        else:
            sequence = raw.replace("\n", "").replace("\r", "")

        analyze(sequence)


if __name__ == "__main__":
    main()
