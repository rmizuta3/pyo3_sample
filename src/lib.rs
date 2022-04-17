use pyo3::prelude::*;
use rand::Rng;

#[pyfunction]
fn annealing(places: Vec<(i32, i32)>, route: Vec<i32>) -> (i32, i32) {
    fn get_time() -> f64 {
        static mut STIME: f64 = -1.0;
        let t = std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap();
        let ms = t.as_secs() as f64 + t.subsec_nanos() as f64 * 1e-9;
        unsafe {
            if STIME < 0.0 {
                STIME = ms;
            }
            ms - STIME
        }
    }

    fn calc_distance(places: &Vec<(i32, i32)>, route: &Vec<i32>) -> i32 {
        let mut dist = 0;
        for i in 0..route.len() - 1 {
            route[i];
            dist += (places[route[i] as usize].0 - places[route[i + 1] as usize].0).abs()
                + (places[route[i] as usize].1 - places[route[i + 1] as usize].1).abs();
        }
        dist
    }

    let start_time = get_time();
    let mut max_cost = calc_distance(&places, &route);
    //let mut route_history = [route];
    let mut loop_count = 0;
    let mut route_result = route.clone();
    loop {
        if get_time() - start_time > 2.0 {
            break;
        }
        loop_count += 1;
        let mut rng = rand::thread_rng();
        let swap_point1 = rng.gen_range(0, 99);
        let swap_point2 = rng.gen_range(0, 99);
        if swap_point1 == swap_point2 {
            continue;
        }
        let mut swap_route = route_result.clone();
        swap_route.swap(swap_point1, swap_point2);
        //let swap_route[swap_point1],swap_route[swap_point2]=route[swap_point2],route[swap_point1]
        let swaproute_cost = calc_distance(&places, &swap_route);
        let randvalue: f64 = rng.gen();
        if swaproute_cost < max_cost || randvalue > 0.99999 {
            route_result = swap_route;
            max_cost = swaproute_cost;
            //route_history.push(route)
            //print(i,max_cost)
        }
    }
    (max_cost, loop_count)
}

#[pymodule]
fn pyo3_salesman(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(annealing, m)?)?;
    Ok(())
}
