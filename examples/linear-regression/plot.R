library(ggplot2)
library(latex2exp)

args <- commandArgs(TRUE)
points <- read.csv(args[1])
line <- read.csv(args[2])

ggplot(
  points,
  aes(
    x=x,
    y=y
  )
) + 
  
  geom_point() +
  geom_line(data=line, color='steelblue') +
  xlab('X') +
  ylab('Y') +

  theme(
    text = element_text(size=15),
    axis.text.x = element_text(size=15),
    axis.text.y = element_text(size=15)
  )

  ggsave(args[3], dpi=300, width=12, height=6)



