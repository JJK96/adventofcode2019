mass_to_fuel mass = (floor $ (fromIntegral mass)/3) -2

fuel_usage input
    | usage < 0 = 0
    | otherwise = usage + fuel_usage usage
    where usage = mass_to_fuel input

one inputs = sum $ map mass_to_fuel inputs

two inputs = sum $ map fuel_usage inputs

main = do
    contents <- readFile "input"
    let inputs = map read $ lines contents
    print $ "1: " ++ show (one inputs)
    print $ "2: " ++ show (two inputs)
