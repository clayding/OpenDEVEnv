#!/bin/bash

/usr/bin/python3 generate.py -k

image_base=docker4dev_base
image_subd=(docker4kernel)

if [ $# != 2 ];
then
echo "Usage:"
echo "  bash $0 <-a/--all/-s/--split> [image name]"
echo "Example:"
echo -e "  bash $0 -s ${image_base}\n\t\t Build ${image_base} only"
for image in ${image_subd[@]}; do
echo -e "  bash $0 -a ${image}\n\t\t Rebuild base and ${image}"
echo -e "  bash $0 -s ${image}\n\t\t Build ${image}"
done
exit 0
fi

options=$1
imagename=$2

if [ "${options}" == "-a" ] || [ "${options}" == "--all" ]; then

docker build --no-cache --network=host -t ${imagename} .

elif [ "${options}" == "-s" ] || [ "${options}" == "--split" ]; then

docker build --no-cache --network=host -t ${imagename} --target ${imagename} .

else
    echo "Option $options is unsupported"
fi
