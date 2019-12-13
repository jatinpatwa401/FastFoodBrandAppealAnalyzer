<?php

namespace App\Http\Controllers;
use DB;
use Illuminate\Http\Request;

use Illuminate\Foundation\Auth\Access\AuthorizesRequests;
use Illuminate\Foundation\Bus\DispatchesJobs;
use Illuminate\Foundation\Validation\ValidatesRequests;
use Illuminate\Routing\Controller as BaseController;
use Illuminate\Support\Arr;



class Controller extends BaseController
{
    use AuthorizesRequests, DispatchesJobs, ValidatesRequests;
    public function mapDashboard()
    {
        # code...
        $data = DB::table('twitter_insights')->distinct('Location')->pluck('Restaurant');
        return view('pages.mapDashboard', ['restaurants' => $data]);
    }

    public function stateDashboard()
    {
        # code...
        $data = DB::table('twitter_insights')->distinct('Location')->pluck('Location');
        return view('pages.stateDashboard', ['states' => $data]);
    }

    public function restaurantDashboard()
    {
        # code...
        $data = DB::table('twitter_insights')->distinct('Location')->pluck('Restaurant');
        return view('pages.restaurantDashboard', ['restaurants' => $data]);
    }

    public function detailDashboard()
    {
        # code...
        $restaurants = DB::table('twitter_insights')->distinct('Location')->pluck('Restaurant');
        $states = DB::table('twitter_insights')->distinct('Location')->pluck('Location');
        return view('pages.detailDashboard')->with('states',$states)->with('restaurants', $restaurants);
    }

    public function manageMap(Request $request) 
    {
        # code...
        $pos_sent = array();
        $neg_sent = array();
        $pos_sar = array();
        $neg_sar = array();
        $popularity = array();
        $negativity = array();
        $data = $request->all();
        $restaurants = DB::table('twitter_insights')->distinct('Restaurant')->pluck('Restaurant');
        $stats = DB::table('twitter_insights')->where('Restaurant', $data['restaurant'])->get();
        $selected = $data['restaurant'];
        foreach ($stats as $key => $stat) {
            $pos_sent = Arr::add($pos_sent, $stat->Location, $stat->NumPosSarcastic);
            $neg_sent = Arr::add($pos_sent, $stat->Location, $stat->NumPosSarcastic);
            $pos_sar = Arr::add($pos_sent, $stat->Location, $stat->NumPosSarcastic);
            $pos_sar = Arr::add($pos_sent, $stat->Location, $stat->NumPosSarcastic);
            $totalpos = $stat->NumPosSentiment + $stat->NumPosSarcastic;
            $totalneg = $stat->NumNegSentiment + $stat->NumNegSarcastic;
            $total = $stat->NumPosSentiment + $stat->NumPosSarcastic + $stat->NumNegSentiment + $stat->NumNegSarcastic;
            // $percent_pos = ($totalpos/$total)*100;
            $percent_pos = $totalpos;
            $percent_neg= ($totalneg/$total)*100;
            $popularity = Arr::add($popularity, $stat->Location, $percent_pos);
            $negativity = Arr::add($negativity, $stat->Location, $percent_neg);
        }
        $mostpos = max($popularity);
        $mostpos_key = array_search($mostpos, $popularity);
        $mostneg = max($popularity);
        $mostneg_key = array_search($mostneg, $popularity);
        // var_dump($popularity);
        return view('pages.mapDashboard')->with('popularity', $popularity)->with('mostpos', $mostpos)->with('mostpos_key', $mostpos_key)->with('restaurants', $restaurants)->with('selected', $selected);
    }

    public function manageDetailData(Request $request)
    {
        # code...
        $data = $request->all();
        $restaurants = DB::table('twitter_insights')->distinct('Location')->pluck('Restaurant');
        $states = DB::table('twitter_insights')->distinct('Location')->pluck('Location');
        $state = $data['state'];
        $restaurant = $data['restaurant'];
        $stats = DB::table('twitter_insights')->select('NumPosSentiment','NumNegSentiment', 'NumPosSarcastic', 'NumNegSarcastic')->where('Restaurant', $data['restaurant'])->where('Location', $data['state'])->first();
        return view('pages.detailDashboard')->with('stats', $stats)->with('selectedstate', $state)->with('selectedrestaurant', $restaurant)->with('states',$states)->with('restaurants', $restaurants);
    }

    public function manageStateData(Request $request) 
    {
        # code...
        $pos_sent = array();
        $neg_sent = array();
        $pos_sar = array();
        $neg_sar = array();
        $popularity = array();
        $negativity = array();
        $data = $request->all();
        $states = DB::table('twitter_insights')->pluck('Location');
        $stats = DB::table('twitter_insights')->where('Location', $data['state'])->get();
        $selected = $data['state'];
        foreach ($stats as $key => $stat) {
            $pos_sent = Arr::add($pos_sent, $stat->Restaurant, $stat->NumPosSarcastic);
            $neg_sent = Arr::add($pos_sent, $stat->Restaurant, $stat->NumPosSarcastic);
            $pos_sar = Arr::add($pos_sent, $stat->Restaurant, $stat->NumPosSarcastic);
            $pos_sar = Arr::add($pos_sent, $stat->Restaurant, $stat->NumPosSarcastic);
            $totalpos = $stat->NumPosSentiment + $stat->NumPosSarcastic;
            $totalneg = $stat->NumNegSentiment + $stat->NumNegSarcastic;
            $total = $stat->NumPosSentiment + $stat->NumPosSarcastic + $stat->NumNegSentiment + $stat->NumNegSarcastic;
            // $percent_pos = ($totalpos/$total)*100;
            $percent_pos = $totalpos;

            $percent_neg= ($totalneg/$total)*100;
            $popularity = Arr::add($popularity, $stat->Restaurant, $percent_pos);
            $negativity = Arr::add($negativity, $stat->Restaurant, $percent_neg);
        }
        $mostpos = max($popularity);
        $mostpos_key = array_search($mostpos, $popularity);
        $mostneg = max($popularity);
        $mostneg_key = array_search($mostneg, $popularity);
        return view('pages.stateDashboard')->with('popularity', $popularity)->with('mostpos', $mostpos)->with('mostpos_key', $mostpos_key)->with('states', $states)->with('selected', $selected);
    }

    public function manageRestaurantData(Request $request) 
    {
        # code...
        $pos_sent = array();
        $neg_sent = array();
        $pos_sar = array();
        $neg_sar = array();
        $popularity = array();
        $negativity = array();
        $data = $request->all();
        $restaurants = DB::table('twitter_insights')->distinct('Restaurant')->pluck('Restaurant');
        $stats = DB::table('twitter_insights')->where('Restaurant', $data['restaurant'])->get();
        $selected = $data['restaurant'];
        foreach ($stats as $key => $stat) {
            $pos_sent = Arr::add($pos_sent, $stat->Location, $stat->NumPosSarcastic);
            $neg_sent = Arr::add($pos_sent, $stat->Location, $stat->NumPosSarcastic);
            $pos_sar = Arr::add($pos_sent, $stat->Location, $stat->NumPosSarcastic);
            $pos_sar = Arr::add($pos_sent, $stat->Location, $stat->NumPosSarcastic);
            $totalpos = $stat->NumPosSentiment + $stat->NumPosSarcastic;
            $totalneg = $stat->NumNegSentiment + $stat->NumNegSarcastic;
            $total = $stat->NumPosSentiment + $stat->NumPosSarcastic + $stat->NumNegSentiment + $stat->NumNegSarcastic;
            // $percent_pos = ($totalpos/$total)*100;
            $percent_pos = $totalpos;

            $percent_neg= ($totalneg/$total)*100;
            $popularity = Arr::add($popularity, $stat->Location, $percent_pos);
            $negativity = Arr::add($negativity, $stat->Location, $percent_neg);
        }
        $mostpos = max($popularity);
        $mostpos_key = array_search($mostpos, $popularity);
        $mostneg = max($popularity);
        $mostneg_key = array_search($mostneg, $popularity);
        return view('pages.restaurantDashboard')->with('popularity', $popularity)->with('mostpos', $mostpos)->with('mostpos_key', $mostpos_key)->with('restaurants', $restaurants)->with('selected', $selected);
    }
}
