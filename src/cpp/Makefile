CXX = mpicxx
CXXFLAGS = -O2 -Wall -std=c++11 `pkg-config --cflags meep`
LDFLAGS = -Wl,-rpath,/usr/local/lib `pkg-config --libs meep`

SRC = multistack.cpp
OBJ = $(SRC:.cpp=.o)
EXEC = multistack

all: $(EXEC)

$(EXEC): $(OBJ)
	$(CXX) $(CXXFLAGS) -o $@ $^ $(LDFLAGS)

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

clean:
	rm -f $(OBJ) $(EXEC)

check-syntax:
	$(CXX) -fsyntax-only $(SOURCES)

run: $(EXEC)
	mpirun -np 4 ./$(EXEC)
