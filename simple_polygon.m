% changed functions which are outdated
function [x, y, dt] = simple_polygon(numSides)

    if numSides < 3
        x = [];
        y = [];
        dt = [];
        return
    end

    oldState = warning('off', 'MATLAB:TriRep:PtsNotInTriWarnId');

    fudge = ceil(numSides/10);
    x = rand(numSides+fudge, 1);
    y = rand(numSides+fudge, 1);

%     dt1 = DelaunayTri(x, y);
    dt = delaunayTriangulation(x, y);
    
    boundaryEdges = freeBoundary(dt);

    % Plot resulting triangulation, not really necessary  
    triplot(dt)
    pause;
    hold on
    plot(x(boundaryEdges),y(boundaryEdges),'-r','LineWidth',2)
    pause;
    
    numEdges = size(boundaryEdges, 1)
    numSides
    while numEdges ~= numSides
        if numEdges > numSides
% Returns the simplices attached to the specified vertices
            triIndex = vertexAttachments(dt, boundaryEdges(:,1));
            triIndex = triIndex(randperm(numel(triIndex)));
            keep = (cellfun('size', triIndex, 2) ~= 1);
            warning('mayor');
        end
        if (numEdges < numSides) || all(keep)
% Returns the simplices attached to the specified edges
            triIndex = edgeAttachments(dt, boundaryEdges);
            triIndex = triIndex(randperm(numel(triIndex)));
            triPoints = dt([triIndex{:}], :);
            keep = all(ismember(triPoints, boundaryEdges(:,1)), 2);
            warning('menor');
        end
        if all(keep)
            warning('Couldn''t achieve desired number of sides!');
            break
        end
%         triPoints = dt.Triangulation;
%         dt1 = TriRep(triPoints, x, y);
        triPoints = dt.ConnectivityList;
        triPoints(triIndex{find(~keep, 1)}, :) = [];
        dt = triangulation(triPoints, x, y);
        boundaryEdges = freeBoundary(dt);
        numEdges = size(boundaryEdges, 1);
    end

    boundaryEdges = [boundaryEdges(:,1); boundaryEdges(1,1)];
%     x = dt.X(boundaryEdges, 1);
%     y = dt.X(boundaryEdges, 2);
    x = dt.Points(boundaryEdges, 1);   
    y = dt.Points(boundaryEdges, 2);

    warning(oldState);

end
