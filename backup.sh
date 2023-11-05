date
echo "making backup"
cp -v /root/python/website-differ/sites.csv "/root/backup/website-differ/sites_$(date +"%Y-%m-%d_%H:%M:%S").csv"
