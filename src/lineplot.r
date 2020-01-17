library(tidyverse)
df <- read.csv(file = 'output.csv', header = FALSE)
df(head)

df %>% 
  rename(
    Clusters = V1,
    Sr_Mode = V2
    )
