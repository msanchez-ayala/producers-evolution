# Producer's Evolution

I hypothesize that musical producers, rather than artists, are the principal
drivers of musical aesthetics in hip-hop/rap. Thus, someone who likes, for
instance, a Drake song that was produced by his main producer, Noah "40" Shebib,
is also very likely to enjoy other songs produced by "40".

I'd like to explore how a particular producer's style evolves over time and use
that information to inform a content-based recommendation system.

[This article](https://www.theringer.com/music/2018/7/3/17529420/drake-scorpion-40-noah-shebib-producers)
kind of gets at the idea.

## Data Sources

I plan to use the Spotify API through `spotipy`, a Python driver to collect song
metadata. However, producer information will need to be garnered from other
sources such as perhaps Wikipedia or wherever I can most easily scrape it.
