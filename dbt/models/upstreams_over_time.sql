SELECT distro, year, (hpd * 365) AS hits_per_year
FROM ldp_stg.rank_by_year
WHERE distro IN ('Debian', 'Fedora', 'Arch', 'openSUSE')