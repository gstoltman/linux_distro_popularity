SELECT distro, (SUM(hpd) * 365) AS est_total_hits
FROM ldp_stg.rank_by_year
GROUP BY distro
ORDER BY (SUM(hpd) * 365) DESC
LIMIT 10