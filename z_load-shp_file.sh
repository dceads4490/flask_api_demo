#!/bin/bash
shp2pgsql /tl_2019_us_state/tl_2019_us_state.shp public.tl_2019_us_state | psql -U testusr testdb
echo "ALTER ROLE testusr WITH PASSWORD 'password';"|psql -U testusr testdb
