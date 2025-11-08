#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Στατιστική Ανάλυση Ερωτηματολογίων
Διπλωματική Καράτζα Παρασκευή - Δήμος Μαραθώνα
Κυκλική Οικονομία και Ανακύκλωση
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams
import glob
import warnings
warnings.filterwarnings('ignore')

# Ρύθμιση για ελληνικά
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# Χρώματα για γραφήματα (eco-friendly palette)
COLORS = ['#2ecc71', '#3498db', '#e74c3c', '#f39c12', '#9b59b6', '#1abc9c', '#34495e', '#95a5a6']
sns.set_palette(COLORS)

class SurveyAnalyzer:
    """Κλάση για την ανάλυση των ερωτηματολογίων"""

    def __init__(self, csv_file):
        """Φόρτωση δεδομένων"""
        self.df = pd.read_csv(csv_file)
        self.n = len(self.df)
        print(f"✓ Φορτώθηκαν {self.n} ερωτηματολόγια")
        print(f"✓ Συνολικές ερωτήσεις: {len(self.df.columns)}")

        # Δημιουργία φακέλων για αποτελέσματα
        import os
        os.makedirs('analysis_output', exist_ok=True)
        os.makedirs('analysis_output/charts', exist_ok=True)
        os.makedirs('analysis_output/tables', exist_ok=True)

        self.results = {}

    def clean_column_names(self):
        """Καθαρισμός ονομάτων στηλών"""
        # Απλοποιημένα ονόματα
        self.col_map = {
            self.df.columns[0]: 'timestamp',
            self.df.columns[1]: 'consent',
            self.df.columns[2]: 'age',
            self.df.columns[3]: 'gender',
            self.df.columns[4]: 'education',
            self.df.columns[5]: 'knows_recycling',
            self.df.columns[6]: 'what_recycles',
            self.df.columns[7]: 'weekly_quantity',
            self.df.columns[8]: 'more_bins_needed',
            self.df.columns[9]: 'knows_collection_freq',
            self.df.columns[10]: 'satisfaction_collection',
            self.df.columns[11]: 'municipality_support',
            self.df.columns[12]: 'how_encourage',
        }

    def analyze_demographics(self):
        """Ανάλυση δημογραφικών χαρακτηριστικών"""
        print("\n" + "="*60)
        print("ΔΗΜΟΓΡΑΦΙΚΑ ΧΑΡΑΚΤΗΡΙΣΤΙΚΑ")
        print("="*60)

        results = {}

        # Ηλικία (Ερώτηση 2)
        age_col = self.df.columns[2]
        age_counts = self.df[age_col].value_counts().sort_index()
        print(f"\nΗλικία (n={self.n}):")
        for age, count in age_counts.items():
            pct = (count/self.n)*100
            print(f"  {age}: {count} ({pct:.1f}%)")

        # Φύλο (Ερώτηση 3)
        gender_col = self.df.columns[3]
        gender_counts = self.df[gender_col].value_counts()
        print(f"\nΦύλο (n={self.n}):")
        for gender, count in gender_counts.items():
            pct = (count/self.n)*100
            print(f"  {gender}: {count} ({pct:.1f}%)")

        # Εκπαίδευση (Ερώτηση 4)
        edu_col = self.df.columns[4]
        edu_counts = self.df[edu_col].value_counts()
        print(f"\nΕπίπεδο Εκπαίδευσης (n={self.n}):")
        for edu, count in edu_counts.items():
            pct = (count/self.n)*100
            print(f"  {edu}: {count} ({pct:.1f}%)")

        results['age'] = age_counts
        results['gender'] = gender_counts
        results['education'] = edu_counts

        self.results['demographics'] = results
        return results

    def plot_demographics(self):
        """Γραφήματα δημογραφικών"""
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))

        # Ηλικία
        age_col = self.df.columns[2]
        self.df[age_col].value_counts().sort_index().plot(
            kind='bar', ax=axes[0], color=COLORS[0], edgecolor='black'
        )
        axes[0].set_title('Κατανομή Ηλικιών', fontsize=14, fontweight='bold')
        axes[0].set_xlabel('Ηλικιακή Ομάδα', fontsize=12)
        axes[0].set_ylabel('Συχνότητα', fontsize=12)
        axes[0].tick_params(axis='x', rotation=45)

        # Φύλο
        gender_col = self.df.columns[3]
        self.df[gender_col].value_counts().plot(
            kind='pie', ax=axes[1], autopct='%1.1f%%', colors=COLORS[1:3],
            startangle=90
        )
        axes[1].set_title('Κατανομή Φύλου', fontsize=14, fontweight='bold')
        axes[1].set_ylabel('')

        # Εκπαίδευση
        edu_col = self.df.columns[4]
        self.df[edu_col].value_counts().plot(
            kind='barh', ax=axes[2], color=COLORS[4], edgecolor='black'
        )
        axes[2].set_title('Επίπεδο Εκπαίδευσης', fontsize=14, fontweight='bold')
        axes[2].set_xlabel('Συχνότητα', fontsize=12)

        plt.tight_layout()
        plt.savefig('analysis_output/charts/01_demographics.png', dpi=300, bbox_inches='tight')
        print("✓ Δημιουργήθηκε: charts/01_demographics.png")
        plt.close()

    def analyze_recycling_knowledge(self):
        """Ανάλυση γνώσης ανακύκλωσης"""
        print("\n" + "="*60)
        print("ΓΝΩΣΗ ΚΑΙ ΠΡΑΚΤΙΚΕΣ ΑΝΑΚΥΚΛΩΣΗΣ")
        print("="*60)

        # Ερώτηση 5: Γνωρίζετε αν γίνεται ανακύκλωση;
        knows_col = self.df.columns[5]
        knows_counts = self.df[knows_col].value_counts()
        print(f"\nΓνώση για ανακύκλωση στην πόλη (n={self.n}):")
        for answer, count in knows_counts.items():
            pct = (count/self.n)*100
            print(f"  {answer}: {count} ({pct:.1f}%)")

        # Ερώτηση 6: Τι ανακυκλώνετε;
        what_col = self.df.columns[6]
        what_counts = self.df[what_col].value_counts()
        print(f"\nΤι ανακυκλώνουν περισσότερο (n={len(self.df[what_col].dropna())}):")
        for item, count in what_counts.head(10).items():
            pct = (count/len(self.df[what_col].dropna()))*100
            print(f"  {item}: {count} ({pct:.1f}%)")

        # Ερώτηση 7: Ποσότητα
        qty_col = self.df.columns[7]
        qty_counts = self.df[qty_col].value_counts()
        print(f"\nΕβδομαδιαία ποσότητα ανακυκλώσιμων (n={len(self.df[qty_col].dropna())}):")
        for qty, count in qty_counts.items():
            pct = (count/len(self.df[qty_col].dropna()))*100
            print(f"  {qty}: {count} ({pct:.1f}%)")

        return {
            'knows': knows_counts,
            'what': what_counts,
            'quantity': qty_counts
        }

    def plot_recycling_knowledge(self):
        """Γραφήματα γνώσης ανακύκλωσης"""
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))

        # Γνώση ανακύκλωσης
        knows_col = self.df.columns[5]
        self.df[knows_col].value_counts().plot(
            kind='pie', ax=axes[0], autopct='%1.1f%%', colors=COLORS,
            startangle=90
        )
        axes[0].set_title('Γνωρίζουν για την ανακύκλωση στην πόλη τους;',
                         fontsize=13, fontweight='bold')
        axes[0].set_ylabel('')

        # Τι ανακυκλώνουν
        what_col = self.df.columns[6]
        self.df[what_col].value_counts().head(8).plot(
            kind='barh', ax=axes[1], color=COLORS[2], edgecolor='black'
        )
        axes[1].set_title('Τι ανακυκλώνουν περισσότερο;', fontsize=13, fontweight='bold')
        axes[1].set_xlabel('Συχνότητα', fontsize=11)

        plt.tight_layout()
        plt.savefig('analysis_output/charts/02_recycling_knowledge.png', dpi=300, bbox_inches='tight')
        print("✓ Δημιουργήθηκε: charts/02_recycling_knowledge.png")
        plt.close()

    def analyze_municipality_services(self):
        """Ανάλυση υπηρεσιών Δήμου"""
        print("\n" + "="*60)
        print("ΑΞΙΟΛΟΓΗΣΗ ΥΠΗΡΕΣΙΩΝ ΔΗΜΟΥ")
        print("="*60)

        # Ερώτηση 8: Χρειάζονται περισσότεροι κάδοι;
        bins_col = self.df.columns[8]
        bins_counts = self.df[bins_col].value_counts()
        print(f"\nΧρειάζονται περισσότεροι κάδοι; (n={len(self.df[bins_col].dropna())}):")
        for answer, count in bins_counts.items():
            pct = (count/len(self.df[bins_col].dropna()))*100
            print(f"  {answer}: {count} ({pct:.1f}%)")

        # Ερώτηση 10: Ικανοποίηση από συχνότητα
        sat_col = self.df.columns[10]
        sat_counts = self.df[sat_col].value_counts()
        print(f"\nΙκανοποίηση από συχνότητα απορριμματοφόρων (n={len(self.df[sat_col].dropna())}):")
        for level, count in sat_counts.items():
            pct = (count/len(self.df[sat_col].dropna()))*100
            print(f"  {level}: {count} ({pct:.1f}%)")

        # Ερώτηση 11: Επαρκής υποστήριξη από Δήμο;
        support_col = self.df.columns[11]
        support_counts = self.df[support_col].value_counts()
        print(f"\nΕπαρκής υποστήριξη από Δήμο για ανακύκλωση; (n={len(self.df[support_col].dropna())}):")
        for answer, count in support_counts.items():
            pct = (count/len(self.df[support_col].dropna()))*100
            print(f"  {answer}: {count} ({pct:.1f}%)")

        return {
            'bins': bins_counts,
            'satisfaction': sat_counts,
            'support': support_counts
        }

    def plot_municipality_services(self):
        """Γραφήματα αξιολόγησης Δήμου"""
        fig, axes = plt.subplots(1, 3, figsize=(16, 5))

        # Περισσότεροι κάδοι
        bins_col = self.df.columns[8]
        self.df[bins_col].value_counts().plot(
            kind='bar', ax=axes[0], color=COLORS[0], edgecolor='black'
        )
        axes[0].set_title('Χρειάζονται περισσότεροι κάδοι;',
                         fontsize=12, fontweight='bold')
        axes[0].set_ylabel('Συχνότητα', fontsize=11)
        axes[0].tick_params(axis='x', rotation=45)

        # Ικανοποίηση
        sat_col = self.df.columns[10]
        self.df[sat_col].value_counts().plot(
            kind='bar', ax=axes[1], color=COLORS[3], edgecolor='black'
        )
        axes[1].set_title('Ικανοποίηση από απορριμματοφόρα',
                         fontsize=12, fontweight='bold')
        axes[1].set_ylabel('Συχνότητα', fontsize=11)
        axes[1].tick_params(axis='x', rotation=45)

        # Υποστήριξη Δήμου
        support_col = self.df.columns[11]
        self.df[support_col].value_counts().plot(
            kind='pie', ax=axes[2], autopct='%1.1f%%', colors=COLORS[4:],
            startangle=90
        )
        axes[2].set_title('Επαρκής υποστήριξη από Δήμο;',
                         fontsize=12, fontweight='bold')
        axes[2].set_ylabel('')

        plt.tight_layout()
        plt.savefig('analysis_output/charts/03_municipality_services.png',
                   dpi=300, bbox_inches='tight')
        print("✓ Δημιουργήθηκε: charts/03_municipality_services.png")
        plt.close()

    def analyze_circular_economy_knowledge(self):
        """Ανάλυση γνώσης εννοιών Κυκλικής Οικονομίας (Ερώτηση 15)"""
        print("\n" + "="*60)
        print("ΓΝΩΣΗ ΕΝΝΟΙΩΝ ΚΥΚΛΙΚΗΣ ΟΙΚΟΝΟΜΙΑΣ")
        print("="*60)

        # Ερώτηση 15 - υπάρχουν πολλές υπο-ερωτήσεις
        concepts = [
            ('ΑΠΕ', 25),
            ('ΧΥΤΑ', 26),
            ('ΧΑΔΑ', 27),
            ('Κυκλική Οικονομία', 28),
            ('Έξυπνη Πόλη', 29),
            ('Βιώσιμη Ανάπτυξη', 30),
            ('Πράσινα Σημεία', 31),
            ('Καύση απορριμμάτων', 32)
        ]

        knowledge_data = {}
        for concept, col_idx in concepts:
            col = self.df.columns[col_idx]
            counts = self.df[col].value_counts()
            print(f"\n{concept}:")
            for level, count in counts.items():
                pct = (count/len(self.df[col].dropna()))*100
                print(f"  {level}: {count} ({pct:.1f}%)")
            knowledge_data[concept] = counts

        return knowledge_data

    def plot_circular_economy_knowledge(self):
        """Γράφημα γνώσης εννοιών ΚΟ"""
        concepts = [
            ('ΑΠΕ', 25),
            ('ΧΥΤΑ', 26),
            ('ΧΑΔΑ', 27),
            ('Κυκλική\nΟικονομία', 28),
            ('Έξυπνη\nΠόλη', 29),
            ('Βιώσιμη\nΑνάπτυξη', 30),
            ('Πράσινα\nΣημεία', 31),
            ('Καύση', 32)
        ]

        # Δημιουργία heatmap για επίπεδο γνώσης
        fig, ax = plt.subplots(figsize=(14, 6))

        knowledge_levels = []
        labels = []
        for label, col_idx in concepts:
            col = self.df.columns[col_idx]
            counts = self.df[col].value_counts()

            # Υπολογισμός μέσου επιπέδου γνώσης (1-5)
            # Καθόλου=1, Λίγο=2, Μέτρια=3, Πολύ=4, Πάρα πολύ=5
            total = 0
            count_total = 0
            for level, freq in counts.items():
                if 'Καθόλου' in str(level) or 'καθόλου' in str(level):
                    total += 1 * freq
                elif 'Λίγο' in str(level) or 'λίγο' in str(level):
                    total += 2 * freq
                elif 'Μέτρια' in str(level) or 'μέτρια' in str(level):
                    total += 3 * freq
                elif 'Πολύ' in str(level) or 'πολύ' in str(level):
                    total += 4 * freq
                elif 'Πάρα' in str(level) or 'πάρα' in str(level):
                    total += 5 * freq
                count_total += freq

            avg_knowledge = total / count_total if count_total > 0 else 0
            knowledge_levels.append(avg_knowledge)
            labels.append(label.replace('\n', ' '))

        # Bar plot
        bars = ax.barh(labels, knowledge_levels, color=COLORS[5], edgecolor='black')
        ax.set_xlabel('Μέσο Επίπεδο Γνώσης (1-5)', fontsize=12, fontweight='bold')
        ax.set_title('Γνώση Εννοιών Κυκλικής Οικονομίας και Περιβάλλοντος',
                    fontsize=14, fontweight='bold')
        ax.set_xlim(0, 5)
        ax.axvline(x=3, color='red', linestyle='--', alpha=0.5, label='Μέτρια γνώση')
        ax.legend()

        # Προσθήκη τιμών στα bars
        for i, (bar, val) in enumerate(zip(bars, knowledge_levels)):
            ax.text(val + 0.1, i, f'{val:.2f}', va='center', fontsize=10)

        plt.tight_layout()
        plt.savefig('analysis_output/charts/04_circular_economy_knowledge.png',
                   dpi=300, bbox_inches='tight')
        print("✓ Δημιουργήθηκε: charts/04_circular_economy_knowledge.png")
        plt.close()

    def analyze_municipality_actions(self):
        """Ανάλυση γνώσης δράσεων Δήμου (Ερώτηση 13)"""
        print("\n" + "="*60)
        print("ΓΝΩΣΗ ΔΡΑΣΕΩΝ ΔΗΜΟΥ ΜΑΡΑΘΩΝΑ")
        print("="*60)

        actions = [
            ('Ανακύκλωση αυτοκινήτων', 13),
            ('Ανακύκλωση ελαστικών', 14),
            ('Ανακύκλωση ορυκτελαίων', 15),
            ('Ανακύκλωση ενδυμάτων-υποδημάτων', 16),
            ('Ανακύκλωση λαμπτήρων', 17),
            ('Ανακύκλωση μαγειρικών ελαίων', 18),
            ('Ανακύκλωση μελανοδοχείων', 19),
            ('Ανακύκλωση μπαταριών', 20),
            ('Ανακύκλωση συσκευασιών-ηλεκτ.ειδών', 21),
            ('Ανακύκλωση φαρμάκων', 22),
        ]

        actions_data = {}
        for action, col_idx in actions:
            col = self.df.columns[col_idx]
            counts = self.df[col].value_counts()
            print(f"\n{action}:")
            for level, count in counts.items():
                pct = (count/len(self.df[col].dropna()))*100
                print(f"  {level}: {count} ({pct:.1f}%)")
            actions_data[action] = counts

        return actions_data

    def plot_municipality_actions(self):
        """Γράφημα γνώσης δράσεων Δήμου"""
        actions = [
            ('Αυτοκίνητα', 13),
            ('Ελαστικά', 14),
            ('Ορυκτέλαια', 15),
            ('Ενδύματα', 16),
            ('Λαμπτήρες', 17),
            ('Μαγ. Έλαια', 18),
            ('Μελανοδοχεία', 19),
            ('Μπαταρίες', 20),
            ('Συσκευασίες', 21),
            ('Φάρμακα', 22),
        ]

        # Υπολογισμός % γνώσης για κάθε δράση
        knowledge_pct = []
        labels = []

        for label, col_idx in actions:
            col = self.df.columns[col_idx]
            # Θεωρούμε "γνωρίζουν" όσους απάντησαν οτιδήποτε εκτός από "Καθόλου"
            knows = 0
            total = 0
            for level, count in self.df[col].value_counts().items():
                total += count
                if 'Καθόλου' not in str(level):
                    knows += count

            pct = (knows / total * 100) if total > 0 else 0
            knowledge_pct.append(pct)
            labels.append(label)

        # Δημιουργία γραφήματος
        fig, ax = plt.subplots(figsize=(12, 7))
        bars = ax.barh(labels, knowledge_pct, color=COLORS[1], edgecolor='black')
        ax.set_xlabel('% Πολιτών που Γνωρίζουν', fontsize=12, fontweight='bold')
        ax.set_title('Γνώση Δράσεων Ανακύκλωσης του Δήμου Μαραθώνα',
                    fontsize=14, fontweight='bold')
        ax.set_xlim(0, 100)

        # Προσθήκη τιμών
        for i, (bar, val) in enumerate(zip(bars, knowledge_pct)):
            ax.text(val + 2, i, f'{val:.1f}%', va='center', fontsize=10)

        plt.tight_layout()
        plt.savefig('analysis_output/charts/05_municipality_actions.png',
                   dpi=300, bbox_inches='tight')
        print("✓ Δημιουργήθηκε: charts/05_municipality_actions.png")
        plt.close()

    def analyze_citizen_practices(self):
        """Ανάλυση πρακτικών πολιτών (Ερώτηση 19)"""
        print("\n" + "="*60)
        print("ΠΡΑΚΤΙΚΕΣ ΠΟΛΙΤΩΝ ΓΙΑ ΚΥΚΛΙΚΗ ΟΙΚΟΝΟΜΙΑ")
        print("="*60)

        practices = [
            ('Ξεχωρίζουν ανακυκλώσιμα (μπλε κάδοι)', 50),
            ('Κομποστοποίηση', 51),
            ('Απόθεση σε ειδικούς χώρους', 52),
            ('Αγορά προϊόντων με ανακυκλώσιμη συσκευασία', 53),
            ('Αγορά βιολογικών προϊόντων', 54),
        ]

        practices_data = {}
        for practice, col_idx in practices:
            col = self.df.columns[col_idx]
            counts = self.df[col].value_counts()
            print(f"\n{practice}:")
            for answer, count in counts.items():
                pct = (count/len(self.df[col].dropna()))*100
                print(f"  {answer}: {count} ({pct:.1f}%)")
            practices_data[practice] = counts

        return practices_data

    def plot_citizen_practices(self):
        """Γράφημα πρακτικών πολιτών"""
        practices = [
            ('Διαχωρισμός\nανακυκλώσιμων', 50),
            ('Κομποστο-\nποίηση', 51),
            ('Ειδικοί\nχώροι', 52),
            ('Ανακυκλώσιμη\nσυσκευασία', 53),
            ('Βιολογικά\nπροϊόντα', 54),
        ]

        yes_pct = []
        labels = []

        for label, col_idx in practices:
            col = self.df.columns[col_idx]
            counts = self.df[col].value_counts()

            yes_count = counts.get('Ναι', 0) + counts.get('ΝΑΙ', 0) + counts.get('ναι', 0)
            total = counts.sum()
            pct = (yes_count / total * 100) if total > 0 else 0

            yes_pct.append(pct)
            labels.append(label.replace('\n', ' '))

        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.bar(range(len(labels)), yes_pct, color=COLORS[2], edgecolor='black')
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels, rotation=15, ha='right')
        ax.set_ylabel('% Πολιτών που Εφαρμόζουν', fontsize=12, fontweight='bold')
        ax.set_title('Πρακτικές Πολιτών για Κυκλική Οικονομία',
                    fontsize=14, fontweight='bold')
        ax.set_ylim(0, 100)
        ax.axhline(y=50, color='red', linestyle='--', alpha=0.5, label='50%')
        ax.legend()

        # Προσθήκη τιμών
        for bar, val in zip(bars, yes_pct):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 2,
                   f'{val:.1f}%', ha='center', va='bottom', fontsize=10)

        plt.tight_layout()
        plt.savefig('analysis_output/charts/06_citizen_practices.png',
                   dpi=300, bbox_inches='tight')
        print("✓ Δημιουργήθηκε: charts/06_citizen_practices.png")
        plt.close()

    def create_summary_report(self):
        """Δημιουργία συνολικής αναφοράς"""
        print("\n" + "="*60)
        print("ΔΗΜΙΟΥΡΓΙΑ ΣΥΝΟΛΙΚΗΣ ΑΝΑΦΟΡΑΣ")
        print("="*60)

        with open('analysis_output/ΑΝΑΦΟΡΑ_ΑΠΟΤΕΛΕΣΜΑΤΩΝ.txt', 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("ΑΠΟΤΕΛΕΣΜΑΤΑ ΕΡΕΥΝΑΣ ΕΡΩΤΗΜΑΤΟΛΟΓΙΟΥ\n")
            f.write("Διπλωματική Εργασία: Καράτζα Παρασκευή-Αικατερίνη\n")
            f.write("Θέμα: Κυκλική Οικονομία και Ανακύκλωση - Δήμος Μαραθώνα\n")
            f.write("="*70 + "\n\n")

            f.write(f"Συνολικός αριθμός ερωτηματολογίων: {self.n}\n")
            f.write(f"Ημερομηνία ανάλυσης: {pd.Timestamp.now().strftime('%d/%m/%Y')}\n\n")

            f.write("ΒΑΣΙΚΑ ΕΥΡΗΜΑΤΑ\n")
            f.write("-"*70 + "\n\n")

            # Demographics
            f.write("1. ΔΗΜΟΓΡΑΦΙΚΑ ΧΑΡΑΚΤΗΡΙΣΤΙΚΑ\n\n")

            gender_col = self.df.columns[3]
            gender_counts = self.df[gender_col].value_counts()
            f.write(f"Φύλο:\n")
            for gender, count in gender_counts.items():
                pct = (count/self.n)*100
                f.write(f"  - {gender}: {count} ({pct:.1f}%)\n")
            f.write("\n")

            # Recycling knowledge
            knows_col = self.df.columns[5]
            knows_yes = self.df[knows_col].value_counts().get('Ναι', 0) + \
                       self.df[knows_col].value_counts().get('ΝΑΙ', 0)
            knows_pct = (knows_yes / len(self.df[knows_col].dropna()) * 100)
            f.write(f"2. ΓΝΩΣΗ ΑΝΑΚΥΚΛΩΣΗΣ\n\n")
            f.write(f"Γνωρίζουν για ανακύκλωση: {knows_pct:.1f}%\n\n")

            # Municipality satisfaction
            support_col = self.df.columns[11]
            f.write(f"3. ΙΚΑΝΟΠΟΙΗΣΗ ΑΠΟ ΔΗΜΟ\n\n")
            support_counts = self.df[support_col].value_counts()
            for answer, count in support_counts.items():
                pct = (count/len(self.df[support_col].dropna()))*100
                f.write(f"  - {answer}: {pct:.1f}%\n")
            f.write("\n")

            f.write("\n" + "="*70 + "\n")
            f.write("ΤΕΛΟΣ ΑΝΑΦΟΡΑΣ\n")
            f.write("="*70 + "\n")

        print("✓ Δημιουργήθηκε: ΑΝΑΦΟΡΑ_ΑΠΟΤΕΛΕΣΜΑΤΩΝ.txt")

    def run_full_analysis(self):
        """Εκτέλεση πλήρους ανάλυσης"""
        print("\n" + "🔍 " + "="*60)
        print("ΕΝΑΡΞΗ ΠΛΗΡΟΥΣ ΣΤΑΤΙΣΤΙΚΗΣ ΑΝΑΛΥΣΗΣ")
        print("="*60 + "\n")

        # Δημογραφικά
        self.analyze_demographics()
        self.plot_demographics()

        # Γνώση ανακύκλωσης
        self.analyze_recycling_knowledge()
        self.plot_recycling_knowledge()

        # Υπηρεσίες Δήμου
        self.analyze_municipality_services()
        self.plot_municipality_services()

        # Γνώση εννοιών ΚΟ
        self.analyze_circular_economy_knowledge()
        self.plot_circular_economy_knowledge()

        # Δράσεις Δήμου
        self.analyze_municipality_actions()
        self.plot_municipality_actions()

        # Πρακτικές πολιτών
        self.analyze_citizen_practices()
        self.plot_citizen_practices()

        # Συνολική αναφορά
        self.create_summary_report()

        print("\n" + "="*60)
        print("✅ ΟΛΟΚΛΗΡΩΘΗΚΕ Η ΑΝΑΛΥΣΗ")
        print("="*60)
        print(f"\nΑποτελέσματα αποθηκευμένα στο φάκελο: analysis_output/")
        print(f"  - Γραφήματα: analysis_output/charts/")
        print(f"  - Αναφορά: analysis_output/ΑΝΑΦΟΡΑ_ΑΠΟΤΕΛΕΣΜΑΤΩΝ.txt")
        print("\n")


def main():
    """Main function"""
    # Εύρεση CSV αρχείου
    csv_files = glob.glob('/home/user/thesis/*.csv')

    if not csv_files:
        print("❌ Δεν βρέθηκε CSV αρχείο!")
        return

    csv_file = csv_files[0]
    print(f"📊 Φόρτωση δεδομένων από: {csv_file}\n")

    # Δημιουργία analyzer και εκτέλεση
    analyzer = SurveyAnalyzer(csv_file)
    analyzer.run_full_analysis()


if __name__ == "__main__":
    main()
