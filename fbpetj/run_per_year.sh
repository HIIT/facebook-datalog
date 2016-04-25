authPath="token.auth"
startYear=2000
finishYear=2017

currentYear=$startYear

# quick test!
python3 fetchEvents.py -a $authPath -s 2016-04-20 -u 2016-04-24

while [ currentYear -le finishYear ]
do
    s=$currentYear-01-01
    u=`expr $currentYear + 1`-01-01
    python3 fetchEvents.py -a $authPath -s $s -u $u
    echo "Processed year "$currentYear", moving on..."

    currentYear = `expr $currentYear + 1`
done

echo "All years fetched! See results!"
