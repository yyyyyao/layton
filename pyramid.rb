#!/usr/bin/env ruby
# -*- coding: utf-8 -*-

################################################################################
# defualt
################################################################################
@@n = 4
@@topdown  = false
@@bottomup = false
@@debug = false

################################################################################
# Arguments
################################################################################
require "optparse"
OptionParser.new { |opts|
  # options
  opts.on("-h","--help","Show this message") {
    puts opts
    exit
  }
  opts.on("-n [INPUT]"){ |f|
    @@n = f.to_i
  }
  opts.on("-t", "--top"){
    @@topdown = true
  }
  opts.on("-b", "--bottom"){
    @@bottomup = true
  }
  opts.on("-d", "--debug"){
    @@debug = true
  }
  # parse
  opts.parse!(ARGV)
}

#### size ####
@@size = @@n * (@@n+1) / 2

################################################################################
# Array
################################################################################
class Array
  #### sum ####
  def sum
    self.inject(:+)
  end
  #### combination ####
  def combination(n)
    return [[]]              if n == 0
    return self.map{|i| [i]} if n == 1

    cs = []
    self.combination(n-1).each do |c|
      i = self.index(c.last)
      self[i+1..-1].each do |e|
        cs.push(c + [e])
      end
    end
    cs
  end
  #### permutation ####
  def permutation(n)
    return [[]]              if n == 0
    return self.map{|i| [i]} if n == 1

    ps = []
    self.permutation(n-1).each do |p|
      (self-p).each do |e|
        ps.push(p + [e])
      end
    end
    ps
  end
end

################################################################################
# util
################################################################################
#### depth ####
def depth(index)
  for n in 0..@@n
    i = n * (n+1) / 2
    return n if index < i
  end
  return -1
end

#### prev sibling ####
# 0: 0
# 1: 1  2
# 2: 3  4  5
# 3: 6  7  8  9
# n: ↑ have no prev sibling
def has_prev_sibling?(index)
  for n in 0..@@n
    i = n * (n+1) / 2
    return false if index == i
  end
  return true
end
def prev_sibling(index)
  index - 1
end

#### next sibling ####
# 0:          0
# 1:       1  2
# 2:    3  4  5
# 3: 6  7  8  9
# n:          ↑ have no next sibling
def has_next_sibling?(index)
  has_prev_sibling?(index + 1)
end
def next_sibling(index)
  index + 1
end

#### parent ####
# 0:       0
# 1:     1 2
# 2:   3 4 5
# 3: 6 7 8 9
def parent(index)
  d = depth(index)
  index - d
end

#### show solution ####
def show(ary)
  puts "#### #{ary} ####"

  for n in 0..@@n-1
    s = n * (n+1) / 2
    t = s + n
    puts "#{ary[s..t]}"
  end
end

################################################################################
# top-down
################################################################################
#### e is addable to ary ####
def addable?(ary, e)
  puts "addable?(#{ary}, #{e})" if @@debug
  i = ary.size
  return true if !has_prev_sibling?(i)
  return true if ary[parent(i)] == (ary[prev_sibling(i)] - e).abs
  false
end

def topdown
  nums = Array.new(@@size){|i| i+1}
  cs = [ [] ]
  while cs.size > 0
    c = cs.shift

    #### c is a solution ####
    if c.size == @@size
      show(c)
      next
    end

    #### expand ####
    (nums - c).each do |e|
      cs.push(c + [e]) if addable?(c, e)
    end
  end
end

################################################################################
# bottom up
################################################################################
def fill(a, i, e)
  puts "fill(#{a}, #{i}, #{e})" if @@debug

  return false if a.index(e) != nil
  a[i] = e
  return true if !has_next_sibling?(i)
  s = next_sibling(i)
  p = parent(s)
  return fill(a, p, (e - a[s]).abs)
end

def bottomup
  nums = Array.new(@@size){|i| i+1}
  seed = Array.new(@@size){|i| 0}
  cs = [ seed ]

  while cs.size > 0
    c = cs.shift

    #### c is a solution ####
    if c.index(0) == nil
      show(c)
      next
    end

    #### expand ####
    (nums - c).each do |e|
      i = @@size - c.reverse.index(0) - 1
      n = c.clone
      cs.push(n) if fill(n, i, e)
    end
  end
end

################################################################################
# main
################################################################################
if @@topdown
  puts "Top-Down Computation"
  t = Time.now
  topdown
  puts "#{Time.now - t} sec"
end

if @@bottomup
  puts "Bottom-Up Computation"
  t = Time.now
  bottomup
  puts "#{Time.now - t} sec"
end
