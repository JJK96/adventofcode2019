import Data.List.Split

insert value addr memory = before ++ value:after
    where (before, _:after) = splitAt addr memory

computer ip memory = case drop ip memory of
    99:_               -> memory
    1:par1:par2:dest:_ -> computer newpos $ insert (memory!!par1 + memory!!par2) dest memory
    2:par1:par2:dest:_ -> computer newpos $ insert (memory!!par1 * memory!!par2) dest memory
    _                  -> error "unknown opcode"
    where newpos = ip+4

compute noun verb input = computer 0 $ insert noun 1 $ insert verb 2 $ input

main = do
    contents <- readFile "input"
    let input = map read $ splitOn "," contents
    let result = compute 12 2 input
    print $ "1: " ++ show (result!!0)
    let (noun, verb) = head [(noun, verb) | noun <- [0..99], verb <- [0..99], (compute noun verb input)!!0 == 19690720]
    print $ "2: " ++ show (100* noun + verb)

