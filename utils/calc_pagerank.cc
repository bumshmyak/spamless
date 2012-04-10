#include <cstdlib>
#include <iostream>
#include <vector>
#include <utility>
#include <algorithm>
#include <cassert>
#include <string>
#include <sstream>
#include <fstream>
#include <cmath>
#include <numeric>
#include <set>
#include <iterator>

using namespace std;
typedef pair<int, int> ii;

const double EPS = 1e-6;

bool equal(double a, double b) {
  return abs(a - b) < EPS;
}

struct ArcHead {
  int head;
  int weight;
};

// Reads graph description from cin and builds graph in memory
void BuildGraph(
    const char* filename,
    vector<int>& begin,
    vector<ArcHead>& neighbors) {
  ifstream in(filename);
  int vertices_count;
  in >> vertices_count;

  // skip '\n'
  {
    string endline;
    getline(in, endline);
  }

  begin.resize(vertices_count + 1);

  string line;
  for (int v = 0; v < vertices_count; ++v) {
    begin[v] = neighbors.size();
    getline(in, line);
    istringstream neighbors_stream(line);
    string s;
    while (neighbors_stream >> s) {
      s[s.find(':')] = ' ';
      istringstream archead_stream(s);
      ArcHead archead;
      archead_stream >> archead.head >> archead.weight;
      neighbors.push_back(archead);
    }
  }
  begin[vertices_count] = neighbors.size();
}

void GetPageRank(
    const vector<int>& begin,
    const vector<ArcHead>& neighbors,
    double alpha,
    const vector<double>& personalization,
    int iterations_count,
    vector<double>& rank) {
  int n = begin.size() - 1;

  vector< vector<double> > r(2, vector<double>(n));
  r[0] = personalization;
  assert(equal(accumulate(r[0].begin(), r[0].end(), 0.0), 1.0));

  int current = 0;
  int next = 1;
  for (int i = 0; i < iterations_count; ++i) {
    double total_rank = accumulate(r[current].begin(), r[current].end(), 0.0);
    assert(equal(total_rank, 1.0));
    
    fill(r[next].begin(), r[next].end(), 0);
    double total_sink_rank = 0;
    
    for (int vertex_index = 0; vertex_index < n; ++vertex_index) {
      int output_edges_count = begin[vertex_index + 1] - begin[vertex_index];
      double& pagerank = r[current][vertex_index];
      double pagerank_to_next = alpha * pagerank / output_edges_count;

      for (int edge_index = begin[vertex_index];
           edge_index < begin[vertex_index + 1];
           ++edge_index) {
        r[next][neighbors[edge_index].head] += pagerank_to_next;
      }
      
      
      // process sink
      if (output_edges_count == 0) {
        total_sink_rank += pagerank;
      }
    }
    
    for (int vertex_index = 0; vertex_index < n; ++vertex_index) {
      r[next][vertex_index] += ((1.0 - alpha) + alpha * total_sink_rank) / n;
    }

    #if 0
    double err = 0;
    for (int vertex_index = 0; vertex_index < n; ++vertex_index) {
      err += abs(r[0][vertex_index] - r[1][vertex_index]);
    }
    cerr << err << endl;
    #endif
    
    swap(current, next);
  }

  rank = r[current];
}

vector<int> GetTopRanked(const vector<double>& rank, int k) {
 vector< pair<double, int> > a(rank.size());
  for (int i = 0; i < a.size(); ++i) {
    a[i] = pair<double, int>(rank[i], i);
  }

  sort(a.rbegin(), a.rend());
  vector<int> res(k);
  for (int i = 0; i < k; ++i) {
    res[i] = a[i].second;
  }
  return res;
}

void ReadPersonalizationVector(
    const char* filename,
    vector<double>& personalization) {
  ifstream in(filename);
  personalization.clear();
  double t;
  while (in >> t) {
    personalization.push_back(t);
  }
}

void GenPersonalizationVector(
    const vector<int>& begin,
    const vector<ArcHead>& neighbors,
    vector<double>& personalization) {
  int n = begin.size() - 1;
  personalization = vector<double>(n, 1.0 / n);
}

int main(int argc, char** argv) {
  vector<int> begin;
  vector<ArcHead> neighbors;
  BuildGraph(argv[1], begin, neighbors);

  vector<double> personalization;
  //ReadPersonalizationVector(argv[2], personalization);
  GenPersonalizationVector(begin, neighbors, personalization);
  
  vector<double> rank;
  GetPageRank(begin, neighbors, 0.85, personalization, 100, rank);

#if 0
  vector<int> top_ranked = GetTopRanked(rank, rank.size());
  copy(top_ranked.begin(), top_ranked.end(), ostream_iterator<int>(cout, "\n"));
#endif
  copy(rank.begin(), rank.end(), ostream_iterator<int>(cout, "\n"));
 
  return 0;
}
