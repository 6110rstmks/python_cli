<?php

define("REPORT_RANKING", 10);

$csv_file = fopen("dummy1.txt","r");

$player_to_ttlScore = createPlayerScoreArray($csv_file);

$avgScore_to_player = calcAvgScore($player_to_ttlScore);

print_r($avgScore_to_player);

outputRanking($avgScore_to_player);

function createPlayerScoreArray($csv_file)
{
    $player_to_ttlScore = [];

    while (! feof($csv_file))
    {
        $row = fgetcsv($csv_file);
    
        $player_id = $row[1];
        $score = $row[2];
    
        if (array_key_exists($player_id, $player_to_ttlScore))
        {
            $player_to_ttlScore[$player_id]['cnt']++;
            $player_to_ttlScore[$player_id]['ttl']+= $score;
    
        } else {
            $player_to_ttlScore[$player_id]['cnt'] = 1;
            $player_to_ttlScore[$player_id]['ttl'] = $score;
        }
    }
    // print_r($player_to_ttlScore);
    fclose($csv_file);

    return $player_to_ttlScore;
}

function calcAvgScore($player_to_ttlScore)
{
    $avgScore_to_player = [];

    foreach($player_to_ttlScore as $player_id => $cnt_and_ttl_array)
    {
        $cnt = $cnt_and_ttl_array['cnt'];
        $ttl = $cnt_and_ttl_array['ttl'];
        $avgscore = intval($ttl / $cnt);
        echo $avgscore;
        echo "\n";


        if (array_key_exists($avgscore, $avgScore_to_player))
        {

            array_push($avgScore_to_player[$avgscore], $player_id);

        } else {
            $avgScore_to_player[$avgscore] = array($player_id);
        }
    }

    return sortPlayersByAvgScore($avgScore_to_player);
}

function sortPlayersByAvgScore($avgScore_to_player)
{
    krsort($avgScore_to_player);
    return $avgScore_to_player;
}

function outputRanking($avgScore_to_player)
{
    $rank = 1;
    foreach ($avgScore_to_player as $avgscore => $playerArray)
    {

        if ($rank > REPORT_RANKING)
        {
            break;
        }

        foreach ($playerArray as $player_id)
        {

            echo $rank .', ' . $player_id . ', ' . $avgscore;
            echo "\n";
        }

        $rank+= count($playerArray);

    }

}

?>