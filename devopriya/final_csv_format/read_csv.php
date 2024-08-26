//open csv file
if (($handle = fopen("files/cities.csv", "r")) !== FALSE) {

    $flag = true;
    $id=1;

    //fetch data from each row
    while (($data = fgetcsv($handle, ",")) !== FALSE) {
        if ($flag) {
            $flag = false;
            continue;
        }

        //get data from each column
        $date_of_service = $data[0];
        $DOS_native = $data[1];
        $date_prescribed = $data[2];
        $date_prescribed_native = $data[3];
        $ndc_brg = $data[4];
        $quantity = $data[5];
        $rx_number = $data[6];

        echo $date_of_service;
        echo $DOS_native;
        echo $date_prescribed;
        echo $date_prescribed_native;
        echo $ndc_brg;
        echo $quantity;
        echo $rx_number;

    }

    fclose($handle);

}
