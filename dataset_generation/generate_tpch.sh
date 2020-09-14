rm -rf ../dbgen/generated_queries
rm -rf generated_equivalent_showplans/

QUERIES_PATH="./queries_simplified/"

cd ../dbgen
cp $QUERIES_PATH/queries_filtered_0/* ./
cd ../dataset_generation
pwd
python3 gen_queries.py -U SA -P Nhhnghia@2889 --generate_queries --num_queries 10 --filter 0
cd ../dbgen
for i in `seq 1 19`
do
	rm $i.sql
done

cp $QUERIES_PATH/queries_filtered_1/* ./
cd ../dataset_generation
pwd
python3 gen_queries.py -U SA -P Nhhnghia@2889 --generate_queries --num_queries 10 --filter 1
cd ../dbgen
for i in `seq 1 19`
do
	rm $i.sql
done

cp $QUERIES_PATH/queries_filtered_2/* ./
cd ../dataset_generation
pwd
python3 gen_queries.py -U SA -P Nhhnghia@2889 --generate_queries --num_queries 10 --filter 2
cd ../dbgen
for i in `seq 1 19`
do
	rm $i.sql
done

cd ../dataset_generation
python3 gen_equivalent_showplans.py -U SA -P Nhhnghia@2889 --num_templates 13
