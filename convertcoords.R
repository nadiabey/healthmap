library(DBI)
library(sf)
con <- dbConnect(RSQLite::SQLite(),'homes.db')
tab <- dbReadTable(con, 'addresses')
X_coords <- list(tab$addy_x)
Y_coords <- list(tab$addy_y)
library(sf)
dots <- rep(NA, length(X_coords[[1]])) # rep creates empty vector/list
# lists are single objects, list[[1]] gets list itself
# after changing length of dots dots[[1]] no longer works??
for (i in 1:length(dots)){
  dots[i][[1]] <- st_point(x = c(X_coords[[1]][i], Y_coords[[1]][i]))
  if (i == length(dots)){
    s <- st_sfc(dots)
  }
}
st_set_crs(s, 2264)
st_crs(s) <- 2264
newpts <- st_transform(s, 4326) 
# https://r-spatial.github.io/sf/reference/st_write.html

st_write(newpts,'ctest.csv', layer_options = "GEOMETRY=AS_XY")
