<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <title>Happy Birthday, Congress!</title>

    <!-- Bootstrap -->
    <link href="css/bootstrap.min.css" rel="stylesheet">

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>
<body>
  <div class="container">
    <div class="row">
      <div class="col-md-12">
        <h1> Happy Birthday Congress!</h1>
      </div>
    </div>
  </div>

  <div class="container">
    <?php
    $conn = new mysqli('db', 'user', 'pass', 'congress');
    $sql = "SELECT * FROM congress_members
JOIN congress_bios ON congress_members.bioguide_id = congress_bios.bioguide_id
WHERE month(congress_members.birthday) = month(current_date) and day(congress_members.birthday) = day(current_date); ";

    $result = $conn->query($sql);
    if ($result->num_rows > 0) {
        // output data of each row
        while($row = $result->fetch_assoc()) {

            if (substr($row['last_name'],-1) != 's') { ?>
              <div class="row">
                <div class="col-md-9">
                  <h2> Today is <?php echo $row['title'].". ". $row['first_name']." ".$row['last_name']."'s". " (".$row['party']. "-".$row['state'].")"?> birthday!</h2>
                  <img src="<?php echo $row['img_src']?>" class="img-responsive" align="left" style="padding-right:10px;">
                  <?php
                    echo $row['bio_text']; ?>
                </div>
              </div>
          <?php
          }
          else { ?>
            <div class="row">
              <div class="col-md-9">
                <h2> Today is <?php echo $row['title'].". ". $row['first_name']." ".$row['last_name']."'". " (".$row['party']. "-".$row['state'].")"?> birthday!</h2>
                <img src="<?php echo $row['img_src']?>" class="img-responsive" align="left" style="padding-right:10px;">
                <?php
                  echo $row['bio_text']; ?>
              </div>
            </div>
          <?php
          }
        }
    }

    else { ?>
      <div class="row">
        <div class="col-md-9">
          <h2> Today is no one's birthday :( </h2>
        </div>
      </div>
          <?php
    }

    ?>
  </div>
</body>
