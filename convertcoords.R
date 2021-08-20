library(DBI)
library(sf)
con <- dbConnect(RSQLite::SQLite(),'homes.db')
updatedtab <- dbReadTable(con, 'matched')
new_X <- list(updatedtab$epsgNC_x) # x coord -> long
new_Y <- list(updatedtab$espgNC_y) # y coord -> lat; misspelled the acronym lol
spots <- rep(NA, length(X_coords[[1]])) # rep creates empty vector/list
# lists are single objects, list[[1]] gets list itself
# after changing length of dots dots[[1]] no longer works??
for (i in 1:length(spots)){
  spots[i][[1]] <- st_point(x = c(as.numeric(new_X[[1]][i]),
                                  as.numeric(new_Y[[1]][i])))
  if (i == length(spots)){
    t <- st_sfc(spots)
  }
}
st_set_crs(t, 2264)
st_crs(t) <- 2264
newpts2 <- st_transform(t, 4326) 
npanum <- list(updatedtab$npa)
res <- list(updatedtab$residence)
types <- list(updatedtab$type)
lat <- list(updatedtab$latitude)
long <- list(updatedtab$longitude)
fac <- list(updatedtab$facility)
add <- list(updatedtab$address)
xy <- st_coordinates(newpts2)
coors <- split(xy, rep(1:ncol(xy), each = nrow(xy)))
placelat <- coors$'2'
placelong <- coors$'1'

ret <- data.frame(
  npas = npanum,
  residences = res,
  bldg_type = types,
  latitudes = lat,
  longitudes = long,
  facility_name = fac,
  facility_address = add,
  facility_latitude = placelat,
  facility_longitude = placelong,
  stringsAsFactors = FALSE
)
colnames(ret) <- c('npa', 'residence', 'bldg_type', 'latitude','longitude',
                   'facility', 'address','fac_latitude','fac_longitude')
out <- dbWriteTable(con, 'wgs', ret, nrows = 50)