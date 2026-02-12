#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Анализ доменов, которые не получили IP-адреса
"""

import re
from collections import defaultdict

def analyze_hosts_file(hosts_file='hosts'):
    """Анализирует файл hosts и извлекает домены без IP."""
    failed_domains = []
    successful_domains = []
    
    with open(hosts_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Ищем комментарии с ошибками
            if 'не удалось определить IP' in line:
                match = re.search(r'#\s*([^\s]+)\s*-', line)
                if match:
                    failed_domains.append(match.group(1))
            # Ищем успешные записи
            elif line and not line.startswith('#') and '\t' in line:
                parts = line.split('\t')
                if len(parts) >= 2:
                    successful_domains.append(parts[1].strip())
    
    return failed_domains, successful_domains

def categorize_domains(domains):
    """Категоризирует домены по типам."""
    categories = defaultdict(list)
    
    # Популярные сервисы и их поддомены
    popular_patterns = {
        'Google/YouTube': ['ggpht.com', 'gvt1.com', 'ytimg.com', 'google'],
        'Instagram': ['instagram', 'igcdn.com', 'igsonar.com', 'igtv.com'],
        'Twitter/X': ['twimg.com', 'twitter'],
        'Discord': ['discord'],
        'Twitch': ['twitch'],
        'TikTok': ['tiktok'],
        'Cloudflare': ['cloudflare'],
        'AWS/Amazon': ['awsstatic.com', 'cloudfront.net', 'amazonaws'],
        'Rutracker': ['rutracker'],
        'Kodik': ['kodik'],
        'Другие CDN': ['cdn', 'static'],
    }
    
    for domain in domains:
        categorized = False
        domain_lower = domain.lower()
        
        for category, patterns in popular_patterns.items():
            for pattern in patterns:
                if pattern in domain_lower:
                    categories[category].append(domain)
                    categorized = True
                    break
            if categorized:
                break
        
        if not categorized:
            categories['Прочие'].append(domain)
    
    return categories

def main():
    print("=" * 70)
    print("📊 АНАЛИЗ ДОМЕНОВ БЕЗ IP-АДРЕСОВ")
    print("=" * 70)
    
    failed, successful = analyze_hosts_file()
    
    print(f"\n📈 Общая статистика:")
    print(f"   Всего доменов: {len(failed) + len(successful)}")
    print(f"   ✅ Успешно резолвлено: {len(successful)} ({len(successful)/(len(failed)+len(successful))*100:.1f}%)")
    print(f"   ❌ Не резолвлено: {len(failed)} ({len(failed)/(len(failed)+len(successful))*100:.1f}%)")
    
    if not failed:
        print("\n🎉 Все домены успешно резолвлены!")
        return
    
    print(f"\n❌ Домены без IP-адресов ({len(failed)}):")
    print("-" * 70)
    
    categories = categorize_domains(failed)
    
    # Сортируем категории по количеству доменов
    sorted_categories = sorted(categories.items(), key=lambda x: len(x[1]), reverse=True)
    
    for category, domains in sorted_categories:
        print(f"\n📁 {category} ({len(domains)} доменов):")
        for domain in sorted(domains):
            print(f"   • {domain}")
    
    # Анализ популярных сайтов
    print("\n" + "=" * 70)
    print("🌟 ПОПУЛЯРНЫЕ СЕРВИСЫ БЕЗ IP:")
    print("=" * 70)
    
    popular_services = {
        'Google/YouTube CDN': ['ggpht.com', 'gvt1.com', 'ytimg.com'],
        'Instagram CDN': ['cdninstagram.com', 'igcdn.com', 'igsonar.com', 'igtv.com'],
        'Twitter/X CDN': ['abd.twimg.com', 'twimg.com', 'ttwstatic.com'],
        'Discord': ['discord-activities.com', 'discord.status', 'discord.tools', 'discordapp.net'],
        'Twitch CDN': ['ext-twitch.tv', 'twitchcdn.net'],
        'TikTok CDN': ['tiktokcdn-us.com', 'tiktokcdn.com', 'tiktokd.net', 'tiktokd.org', 
                       'tiktokv.us', 'tiktokw.us', 'tik-tokapi.com'],
        'AWS CDN': ['awsstatic.com', 'cloudfront.net'],
        'Cloudflare': ['cloudflare-ipfs.com', 'cloudflareapps.com', 'cloudflarebolt.com',
                       'cloudflarepartners.com', 'cloudflareresolve.com', 'cloudflaretest.com'],
        'Rutracker': ['rutracker.cc', 'rutracker.cloud', 'rutracker.cr', 'rutracker.is'],
        'Стриминг': ['10tv.app', '7tv.gg', 'kodik-storage.com', 'player-aksor.yani.tv',
                     'rezka.fl', 'soundcloud.cloud', 'muscdn.com'],
    }
    
    for service, patterns in popular_services.items():
        found = [d for d in failed if any(p in d.lower() for p in patterns)]
        if found:
            print(f"\n🔴 {service}: {len(found)} доменов")
            for domain in sorted(found):
                print(f"   • {domain}")
    
    # Рекомендации
    print("\n" + "=" * 70)
    print("💡 РЕКОМЕНДАЦИИ:")
    print("=" * 70)
    print("""
1. Многие домены без IP - это CDN поддомены, которые могут использовать динамические IP
2. Некоторые домены могут быть заблокированы на уровне DNS провайдера
3. Для улучшения резолва установите: pip install dnspython
4. Попробуйте запустить скрипт с VPN или другим DNS сервером
5. Некоторые домены могут не существовать или быть неактивными
    """)

if __name__ == '__main__':
    main()
