library(ggplot2)
library(latex2exp)

args <- commandArgs(TRUE)
points_a_filepath <- args[1]
points_b_filepath <- args[2]
output_filepath <- args[3]

points_a <- read.csv(points_a_filepath)
points_b <- read.csv(points_b_filepath)

ggplot(
  points_a,
  aes(
    x=x,
    y=y
  )
) + 
  
  geom_line(colour='grey') +
  geom_line(data=points_b,colour='red') + 
  xlab('X') +
  ylab('Y') +

  theme(
    text = element_text(size=15),
    axis.text.x = element_text(size=15),
    axis.text.y = element_text(size=15)
  )

  ggsave(output_filepath, dpi=300, width=12, height=6)
