module Lib
    ( someFunc
    ) where

someFunc :: IO ()
someFunc = do
    putStrLn "who are you?"
    name <- getLine
    if name == "michael" then
        putStrLn "oh, the greatest"
    else do
        putStrLn "is that all?"
        answer <- getLine
        if answer == "9001" then
            putStrLn "not so bad"
        else
            putStrLn "meh."
