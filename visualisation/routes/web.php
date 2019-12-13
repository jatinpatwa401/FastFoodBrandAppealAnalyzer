<?php

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

Route::get('/', function () {
    return view('welcome');
});

Route::get('/stateDashboard', 'Controller@stateDashboard');

Route::post('/viewStateData', 'Controller@manageStateData');

Route::get('/restaurantDashboard', 'Controller@restaurantDashboard');

Route::post('/viewRestaurantData', 'Controller@manageRestaurantData');

Route::get('/mapDashboard', 'Controller@mapDashboard');

Route::post('/viewMap', 'Controller@manageMap');

Route::get('/detailDashboard', 'Controller@detailDashboard');

Route::post('/viewDetailData', 'Controller@manageDetailData');




