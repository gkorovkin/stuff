{-# LANGUAGE ParallelListComp #-}
import Control.Monad

main = times 200 (compute 1000000) >>= print
	 where
		times n m = do
			  results <- replicateM n m
			  return $ head results

compute n = do
		let xs = [0 .. (n-1)]
		let	ys = [x + k | x <- xs | k <- drop 1 xs]
		return $ sum $ every 100 ys
		where
			every :: Int -> [Int] -> [Int]
			every n [] = []
			every n (x:xs) = x : ( every n $ drop (n-1) xs)