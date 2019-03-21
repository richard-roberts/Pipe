library(ggplot2)
library(latex2exp)

args <- commandArgs(TRUE)
points_filepath <- args[1]
output_filepath <- args[2]

points <- read.csv(points_filepath)

ggplot(
  points,
  aes(
    x=x,
    y=y
  )
) + 
  
  geom_line() +
  xlab('X') +
  ylab('Y') +

  theme(
    text = element_text(size=15),
    axis.text.x = element_text(size=15),
    axis.text.y = element_text(size=15)
  )

  ggsave(output_filepath, dpi=300, width=12, height=6)
