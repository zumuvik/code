#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Анализ паттернов неудачных доменов для поиска похожих
"""

import re
from collections import defaultdict

def analyze_failed_patterns(hosts_file='hosts'):
    """Анализирует паттерны неудачных доменов."""
    failed_domains = []
    successful_domains = {}
    
    with open(hosts_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if 'не удалось определить IP' in line:
                match = re.search(r'#\s*([^\s]+)\s*-', line)
                if match:
                    failed_domains.append(match.group(1))
            elif line and not line.startswith('#') and '\t' in line:
                parts = line.split('\t')
                if len(parts) >= 2:
                    domain = parts[1].strip()
                    ip = parts[0].strip()
                    successful_domains[domain] = ip
    
    print(f"Неудачных доменов: {len(failed_domains)}")
    print(f"Успешных доменов: {len(successful_domains)}")
    
    # Анализ паттернов
    patterns = defaultdict(list)
    
    for failed in failed_domains[:1000]:  # Анализируем первые 1000
        # Извлекаем базовое имя (без TLD)
        parts = failed.split('.')
        if len(parts) >= 2:
            base = '.'.join(parts[:-1])
            tld = parts[-1]
            
            # Ищем похожие домены в успешных
            similar = []
            for success_domain, success_ip in successful_domains.items():
                success_parts = success_domain.split('.')
                if len(success_parts) >= 2:
                    success_base = '.'.join(success_parts[:-1])
                    success_tld = success_parts[-1]
                    
                    # Проверяем разные варианты похожести
                    if base == success_base and tld != success_tld:
                        similar.append((success_domain, success_ip, 'разный TLD'))
                    elif base.startswith(success_base) or success_base.startswith(base):
                        if abs(len(base) - len(success_base)) <= 3:
                            similar.append((success_domain, success_ip, 'похожее имя'))
            
            if similar:
                patterns[failed] = similar[:3]  # Берем первые 3 похожих
    
    print(f"\nНайдено доменов с похожими: {len(patterns)}")
    
    # Показываем примеры
    print("\nПримеры:")
    for i, (failed, similars) in enumerate(list(patterns.items())[:20]):
        print(f"\n{failed}:")
        for similar_domain, similar_ip, reason in similars:
            print(f"  → {similar_domain} ({similar_ip}) - {reason}")
    
    return failed_domains, successful_domains, patterns

if __name__ == '__main__':
    analyze_failed_patterns()
