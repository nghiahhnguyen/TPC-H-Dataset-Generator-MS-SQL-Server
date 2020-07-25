rm -rf ../dbgen/generated_queries
rm -rf generated_equivalent_showplans/

cd ../dbgen
cp queries_filtered_0/* ./
cd ../dataset_generation
pwd
python3 gen_queries.py -U SA -P Nhhnghia@2889 --generate_queries --num_queries 10 --filter 0
cd ../dbgen
for i in `seq 1 22`
do
	rm $i.sql
done

cp queries_filtered_1/* ./
cd ../dataset_generation
pwd
python3 gen_queries.py -U SA -P Nhhnghia@2889 --generate_queries --num_queries 10 --filter 1
cd ../dbgen
for i in `seq 1 22`
do
	rm $i.sql
done

cp queries_filtered_2/* ./
cd ../dataset_generation
pwd
python3 gen_queries.py -U SA -P Nhhnghia@2889 --generate_queries --num_queries 10 --filter 2
cd ../dbgen
for i in `seq 1 22`
do
	rm $i.sql
done

cd ../dataset_generation
python3 gen_equivalent_showplans.py -U SA -P Nhhnghia@2889
